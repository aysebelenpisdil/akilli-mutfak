"""
RAG Pipeline Service
Coordinates Retriever (FAISS) → Reranker → Personalization → Generator (LLM) pipeline
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from app.services.faiss_service import faiss_service
from app.services.embedding_service import embedding_service
from app.services.reranker_service import reranker_service
from app.services.llm_service import llm_service
from app.services.recipe_service import recipe_service
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
        recipe_service=recipe_service
    ):
        self.retriever = faiss_service
        self.embedder = embedding_service
        self.reranker = reranker_service
        self.generator = llm_service
        self.recipe_service = recipe_service

    def _retrieve(self, user_ingredients: List[str], top_k: int = 50) -> List[Recipe]:
        try:
            logger.debug(f"Retrieving top-{top_k} recipes for ingredients: {user_ingredients}")

            if not self.retriever.is_loaded():
                logger.warning("FAISS index not loaded, falling back to string matching")
                results = self.recipe_service.find_suitable_recipes(
                    user_ingredients=user_ingredients, use_vector_search=False, top_k=top_k
                )
                return [Recipe(**recipe.dict()) for recipe in results]

            distances, indices = self.retriever.search_by_ingredients(
                ingredients=user_ingredients,
                k=min(top_k, self.recipe_service.get_total_count()),
                embedding_service=self.embedder
            )

            all_recipes = self.recipe_service.get_all_recipes(
                limit=self.recipe_service.get_total_count()
            )
            retrieved_recipes = [all_recipes[idx] for idx in indices if idx < len(all_recipes)]
            logger.debug(f"Retrieved {len(retrieved_recipes)} recipes from FAISS")
            return retrieved_recipes

        except Exception as e:
            logger.error(f"Error in retrieval step: {e}", exc_info=True)
            logger.warning("Falling back to string matching")
            results = self.recipe_service.find_suitable_recipes(
                user_ingredients=user_ingredients, use_vector_search=False, top_k=top_k
            )
            return [Recipe(**recipe.dict()) for recipe in results]

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
            logger.error(f"Error in reranking step: {e}", exc_info=True)
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
            if delta != 0.0:
                logger.debug(f"[personalization] {recipe.Title}: {score:.3f} + {delta:+.2f} ({interaction})")
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
            logger.error(f"Error in generation step: {e}", exc_info=True)
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
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: Retrieve → Rerank → Personalize → Generate

        user_history: {recipe_title: most_recent_interaction_type} — pre-fetched
                      by the caller (route) from the database.
        """
        personalized = bool(user_history)
        logger.info(
            f"RAG pipeline started: {len(user_ingredients)} ingredients, "
            f"top_k={top_k}, personalized={personalized}"
        )

        # Step 1: Retrieval
        retrieved_recipes = self._retrieve(user_ingredients=user_ingredients, top_k=retrieval_top_k)
        if not retrieved_recipes:
            return {
                "recipes": [],
                "explanation": None,
                "metadata": {
                    "retrieval_count": 0, "reranked_count": 0,
                    "pipeline_stages": ["retrieval"],
                    "retriever_used": False, "reranker_used": False,
                    "llm_used": False, "personalized": False,
                }
            }

        # Step 2: Reranking
        reranked_results = self._rerank(
            user_ingredients=user_ingredients, recipes=retrieved_recipes, top_k=top_k
        )

        # Step 3: Personalization (history-based score adjustment)
        if user_history:
            reranked_results = self._apply_history_scores(reranked_results, user_history)

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
        if personalized:
            stages.append("personalization")
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
            }
        }


rag_pipeline = RAGPipeline()
