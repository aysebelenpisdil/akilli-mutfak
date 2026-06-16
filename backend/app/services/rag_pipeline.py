"""
RAG Pipeline Service
Coordinates Retriever (FAISS) → Reranker → Personalization → Generator (LLM) pipeline
"""

import logging
import math
from typing import List, Optional, Dict, Any, Tuple
from app.services.faiss_service import faiss_service
from app.services.embedding_service import embedding_service
from app.services.reranker_service import reranker_service
from app.services.llm_service import llm_service
from app.services.recipe_service import recipe_service
from app.services.tfidf_service import tfidf_service
from app.models.recipe import Recipe, RecipeWithMatch, MatchScore

logger = logging.getLogger(__name__)

# Score delta applied per interaction type (added to cross-encoder score)
_HISTORY_ADJUSTMENTS: Dict[str, float] = {
    "like":  0.20,
    "cook":  0.25,
    "save":  0.10,
    "view":  0.00,
    "skip": -0.30,
}


class RAGPipeline:
    """
    RAG Pipeline:
    1. Retriever (FAISS) - Vector similarity search
    2. Reranker (Cross-encoder) - Contextual re-ranking
    3. Personalization - History-based score adjustment
    4. Generator (Gemini LLM) - Explanation generation with memory
    """

    def __init__(
        self,
        faiss_service=faiss_service,
        embedding_service=embedding_service,
        reranker_service=reranker_service,
        llm_service=llm_service,
        recipe_service=recipe_service,
        tfidf_service=tfidf_service,
    ):
        self.retriever = faiss_service
        self.embedder = embedding_service
        self.reranker = reranker_service
        self.generator = llm_service
        self.recipe_service = recipe_service
        self.tfidf = tfidf_service

    @staticmethod
    def _rrf_fuse(
        ranked_lists: List[List[int]],
        top_k: int,
        rrf_k: int = 60,
    ) -> List[int]:
        """Reciprocal Rank Fusion: birden fazla sıralı index listesini birleştirir."""
        scores: Dict[int, float] = {}
        for ranked in ranked_lists:
            for rank, idx in enumerate(ranked):
                scores[idx] = scores.get(idx, 0.0) + 1.0 / (rrf_k + rank + 1)
        fused = sorted(scores.items(), key=lambda x: -x[1])
        return [idx for idx, _ in fused[:top_k]]

    def _retrieve(
        self, user_ingredients: List[str], top_k: int = 50, use_hybrid: bool = True
    ) -> Tuple[List[Recipe], bool]:
        """
        Returns (recipes, tfidf_used).
        use_hybrid=True: FAISS + TF-IDF → RRF fusion.
        use_hybrid=False: FAISS-only (A/B karşılaştırması için).
        Her ikisi de yüklü değilse string matching fallback'e düşer.
        """
        try:
            logger.debug(f"Retrieving top-{top_k} recipes for ingredients: {user_ingredients}")

            faiss_loaded = self.retriever.is_loaded()
            tfidf_loaded = self.tfidf.is_loaded() and use_hybrid

            # Her ikisi de yüklü → hibrit RRF
            if faiss_loaded and tfidf_loaded:
                all_recipes = self.recipe_service.get_all_recipes(
                    limit=self.recipe_service.get_total_count()
                )
                n = len(all_recipes)

                _, faiss_indices = self.retriever.search_by_ingredients(
                    ingredients=user_ingredients,
                    k=min(top_k, n),
                    embedding_service=self.embedder,
                )
                _, tfidf_indices = self.tfidf.search_by_ingredients(
                    ingredients=user_ingredients, k=min(top_k, n)
                )

                fused_indices = self._rrf_fuse(
                    [list(faiss_indices), list(tfidf_indices)],
                    top_k=top_k,
                    rrf_k=60,
                )
                retrieved = [all_recipes[i] for i in fused_indices if i < n]
                logger.debug(
                    f"Hybrid RRF: {len(faiss_indices)} FAISS + "
                    f"{len(tfidf_indices)} TF-IDF → {len(retrieved)} fused"
                )
                return retrieved, True

            # Sadece FAISS
            if faiss_loaded:
                all_recipes = self.recipe_service.get_all_recipes(
                    limit=self.recipe_service.get_total_count()
                )
                _, indices = self.retriever.search_by_ingredients(
                    ingredients=user_ingredients,
                    k=min(top_k, len(all_recipes)),
                    embedding_service=self.embedder,
                )
                retrieved = [all_recipes[i] for i in indices if i < len(all_recipes)]
                logger.debug(f"FAISS-only: {len(retrieved)} recipes")
                return retrieved, False

            # Sadece TF-IDF
            if tfidf_loaded:
                all_recipes = self.recipe_service.get_all_recipes(
                    limit=self.recipe_service.get_total_count()
                )
                _, indices = self.tfidf.search_by_ingredients(
                    ingredients=user_ingredients, k=min(top_k, len(all_recipes))
                )
                retrieved = [all_recipes[i] for i in indices if i < len(all_recipes)]
                logger.debug(f"TF-IDF-only: {len(retrieved)} recipes")
                return retrieved, True

            # String matching fallback
            logger.warning("FAISS ve TF-IDF yüklü değil, string matching fallback kullanılıyor")
            results = self.recipe_service.find_suitable_recipes(
                user_ingredients=user_ingredients, use_vector_search=False, top_k=top_k
            )
            return [Recipe(**r.dict()) for r in results], False

        except Exception as e:
            logger.exception(f"Error in retrieval step: {e}")
            logger.warning("Falling back to string matching")
            results = self.recipe_service.find_suitable_recipes(
                user_ingredients=user_ingredients, use_vector_search=False, top_k=top_k
            )
            return [Recipe(**r.dict()) for r in results], False

    def _rerank(
        self,
        user_ingredients: List[str],
        recipes: List[Recipe],
        top_k: int = 10
    ) -> List[Tuple[Recipe, float]]:
        try:
            if not recipes:
                logger.warning("No recipes to rerank")
                return []

            logger.debug(f"Reranking {len(recipes)} recipes to top-{top_k}")
            reranked_results = self.reranker.rerank_by_ingredients(
                ingredients=user_ingredients, recipes=recipes, top_k=top_k
            )
            logger.debug(f"Reranking completed: {len(reranked_results)} top results")
            return reranked_results

        except Exception as e:
            logger.exception(f"Error in reranking step: {e}")
            logger.warning("Falling back to original order")
            return [(recipe, 1.0) for recipe in recipes[:top_k]]

    def _apply_history_scores(
        self,
        reranked: List[Tuple[Recipe, float]],
        user_history: Dict[str, str],
    ) -> List[Tuple[Recipe, float]]:
        """Adjust cross-encoder scores using per-recipe interaction history, then re-sort."""
        adjusted = []
        for recipe, score in reranked:
            interaction = user_history.get(recipe.Title)
            delta = _HISTORY_ADJUSTMENTS.get(interaction, 0.0) if interaction else 0.0
            if not math.isclose(delta, 0.0, abs_tol=1e-9):
                logger.debug(f"[personalization] {recipe.Title}: {score:.3f} + {delta:+.2f} ({interaction})")
            adjusted.append((recipe, score + delta))
        adjusted.sort(key=lambda x: x[1], reverse=True)
        return adjusted

    def _apply_cf_scores(
        self,
        reranked: List[Tuple[Recipe, float]],
        cf_scores: Dict[str, float],
    ) -> List[Tuple[Recipe, float]]:
        """Benzer kullanıcıların tercihleriyle hesaplanan CF deltasını skora ekle."""
        adjusted = []
        for recipe, score in reranked:
            delta = cf_scores.get(recipe.Title, 0.0)
            if not math.isclose(delta, 0.0, abs_tol=1e-9):
                logger.debug(f"[CF] {recipe.Title}: {score:.3f} + {delta:+.3f}")
            adjusted.append((recipe, score + delta))
        adjusted.sort(key=lambda x: x[1], reverse=True)
        return adjusted

    def _generate(
        self,
        user_ingredients: List[str],
        reranked_recipes: List[Tuple[Recipe, float]],
        user_preferences: Optional[Dict[str, Any]] = None,
        excluded_ingredients: Optional[List[str]] = None,
        user_history: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        try:
            if not reranked_recipes:
                logger.warning("No recipes provided for explanation generation")
                return None

            recipes = [recipe for recipe, score in reranked_recipes]
            logger.debug(f"Generating explanation for {len(recipes)} recipes")

            explanation = self.generator.generate_explanation(
                user_ingredients=user_ingredients,
                recommended_recipes=recipes,
                user_preferences=user_preferences,
                excluded_ingredients=excluded_ingredients,
                user_history=user_history,
            )

            if explanation:
                logger.debug(f"Explanation generated: {len(explanation)} characters")
            return explanation

        except Exception as e:
            logger.exception(f"Error in generation step: {e}")
            return None

    def process(
        self,
        user_ingredients: List[str],
        user_preferences: Optional[Dict[str, Any]] = None,
        excluded_ingredients: Optional[List[str]] = None,
        top_k: int = 10,
        explain: bool = True,
        retrieval_top_k: int = 50,
        user_id: Optional[str] = None,
        user_history: Optional[Dict[str, str]] = None,
        cf_scores: Optional[Dict[str, float]] = None,
        use_hybrid: bool = True,
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: Retrieve → Rerank → Personalize → Generate

        user_history: {recipe_title: most_recent_interaction_type} — pre-fetched
                      by the caller (route) from the database.
        """
        personalized = bool(user_history)
        cf_used = bool(cf_scores)
        logger.info(
            f"RAG pipeline started: {len(user_ingredients)} ingredients, "
            f"top_k={top_k}, personalized={personalized}, cf={cf_used}, hybrid={use_hybrid}"
        )

        # Step 1: Retrieval
        retrieved_recipes, tfidf_used = self._retrieve(
            user_ingredients=user_ingredients, top_k=retrieval_top_k, use_hybrid=use_hybrid
        )
        if not retrieved_recipes:
            return {
                "recipes": [],
                "explanation": None,
                "metadata": {
                    "retrieval_count": 0, "reranked_count": 0,
                    "pipeline_stages": ["retrieval"],
                    "retriever_used": False, "reranker_used": False,
                    "llm_used": False, "personalized": False,
                    "tfidf_used": False,
                }
            }

        # Step 2: Reranking
        reranked_results = self._rerank(
            user_ingredients=user_ingredients, recipes=retrieved_recipes, top_k=top_k
        )

        # Step 3a: Personalization (direct interaction history)
        if user_history:
            reranked_results = self._apply_history_scores(reranked_results, user_history)

        # Step 3b: Collaborative filtering (similar users' preferences)
        if cf_scores:
            reranked_results = self._apply_cf_scores(reranked_results, cf_scores)

        # Build RecipeWithMatch list
        final_recipes = []
        for recipe, score in reranked_results:
            recipe_ingredients_lower = recipe.Ingredients.lower()
            matching_ingredients = [
                ing for ing in user_ingredients
                if ing.lower() in recipe_ingredients_lower
            ]
            final_recipes.append(
                RecipeWithMatch(
                    **recipe.dict(),
                    matchingCount=len(matching_ingredients),
                    matchingIngredients=matching_ingredients,
                )
            )

        # Step 4: Generation
        explanation = None
        if explain:
            explanation = self._generate(
                user_ingredients=user_ingredients,
                reranked_recipes=reranked_results,
                user_preferences=user_preferences,
                excluded_ingredients=excluded_ingredients,
                user_history=user_history,
            )

        logger.info(
            f"RAG pipeline completed: {len(final_recipes)} recipes, "
            f"explanation={'yes' if explanation else 'no'}"
        )

        total_ingredients = len(user_ingredients)
        best_match = max((r.matchingCount for r in final_recipes), default=0)
        match_score = MatchScore(
            best_match_count=best_match,
            total_ingredients=total_ingredients,
            label=f"{best_match}/{total_ingredients} malzeme mevcut",
        )

        stages = ["retrieval", "reranking"]
        if tfidf_used:
            stages.append("tfidf_hybrid")
        if personalized:
            stages.append("personalization")
        if cf_used:
            stages.append("collaborative_filtering")
        if explain:
            stages.append("generation")

        return {
            "recipes": final_recipes,
            "explanation": explanation,
            "match_score": match_score,
            "metadata": {
                "retrieval_count": len(retrieved_recipes),
                "reranked_count": len(reranked_results),
                "pipeline_stages": stages,
                "retriever_used": self.retriever.is_loaded(),
                "reranker_used": self.reranker.is_loaded(),
                "llm_used": self.generator.is_available(),
                "personalized": personalized,
                "cf_used": cf_used,
                "tfidf_used": tfidf_used,
            }
        }


rag_pipeline = RAGPipeline()
