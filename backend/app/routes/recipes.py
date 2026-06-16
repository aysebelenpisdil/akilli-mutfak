from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List, Optional
import time
import logging
from app.middleware.rate_limiter import limiter
from app.models.recipe import (
    Recipe,
    RecipeWithMatch,
    RecipeRecommendRequest,
    RecipeRecommendResponse,
    RecipeSearchRequest,
    RecipeSearchResponse,
    RAGRecommendRequest,
    RAGRecommendResponse,
    DietaryPreferences,
    SubstitutionRequest,
    SubstitutionResponse,
    MatchScore,
)
from app.services.recipe_service import recipe_service
from app.services.faiss_service import faiss_service
from app.services.embedding_service import embedding_service
from app.services.rag_pipeline import rag_pipeline
from app.services.llm_service import llm_service
from app.services.database_service import database_service
from app.services.cf_service import cf_service
from app.middleware.auth import get_optional_user

# Setup logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=dict)
async def get_recipes(
    ingredients: Optional[str] = Query(None, description="Comma-separated list of ingredients"),
    q: Optional[str] = Query(None, description="Title substring search"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """
    Get all recipes with optional filtering by ingredients or title substring
    """
    try:
        if ingredients:
            # Filter by ingredients
            ingredient_list = [ing.strip() for ing in ingredients.split(',')]
            filtered_recipes = recipe_service.find_suitable_recipes(ingredient_list)
        else:
            filtered_recipes = recipe_service.get_all_recipes(limit=500, offset=0)

        if q:
            filtered_recipes = [r for r in filtered_recipes if q.lower() in r.Title.lower()]

        total = len(filtered_recipes)
        recipes = filtered_recipes[offset:offset + limit]

        return {
            "recipes": recipes,
            "total": total,
            "count": len(recipes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tarifler alınamadı: {str(e)}")


@router.get("/{title}", response_model=Recipe)
async def get_recipe(title: str):
    """
    Get a specific recipe by title
    """
    try:
        recipe = recipe_service.get_recipe_by_title(title)
        
        if not recipe:
            raise HTTPException(status_code=404, detail="Tarif bulunamadı")
        
        return recipe
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tarif alınamadı: {str(e)}")


@router.post("/recommend", response_model=RecipeRecommendResponse)
@limiter.limit("30/minute")
async def recommend_recipes(request: Request, body: RecipeRecommendRequest):
    """
    Get recipe recommendations based on fridge ingredients using vector search
    
    Uses FAISS vector search if available, falls back to string matching.
    """
    start_time = time.time()
    
    try:
        if not body.ingredients:
            raise HTTPException(status_code=400, detail="Malzeme listesi gerekli")

        # Determine search method
        use_vector_search = body.use_vector_search if body.use_vector_search is not None else True
        top_k = body.top_k if body.top_k is not None else 50

        # Check if vector search is available
        search_method = "vector" if (use_vector_search and faiss_service.is_loaded()) else "string_matching"

        logger.info(f"Recipe recommendation request: {len(body.ingredients)} ingredients, method: {search_method}")

        # Get recommendations
        recommendations = recipe_service.find_suitable_recipes(
            user_ingredients=body.ingredients,
            use_vector_search=use_vector_search,
            top_k=top_k
        )

        process_time = time.time() - start_time
        logger.info(f"Recommendations generated in {process_time:.3f}s: {len(recommendations)} results")

        return RecipeRecommendResponse(
            recommendations=recommendations,
            count=len(recommendations),
            userIngredients=body.ingredients,
            search_method=search_method
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Öneriler oluşturulamadı: {str(e)}")


@router.post("/search", response_model=RecipeSearchResponse)
@limiter.limit("30/minute")
async def search_recipes(request: Request, body: RecipeSearchRequest):
    """
    Search recipes by text query using vector similarity search
    
    Example queries:
    - "spicy chicken pasta"
    - "vegetarian dessert"
    - "quick breakfast recipe"
    """
    start_time = time.time()
    
    try:
        if not body.query or not body.query.strip():
            raise HTTPException(status_code=400, detail="Arama sorgusu gerekli")

        top_k = body.top_k if body.top_k is not None else 20

        # Check if vector search is available
        if faiss_service.is_loaded():
            try:
                logger.info(f"Text search request: '{body.query}', method: vector")

                # Search using FAISS
                distances, indices = faiss_service.search_by_text(
                    text=body.query,
                    k=min(top_k, recipe_service.get_total_count()),
                    embedding_service=embedding_service
                )

                # Convert results to RecipeWithMatch
                results = []
                recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())

                for idx, dist in zip(indices, distances):
                    if idx < len(recipes):
                        recipe = recipes[idx]
                        results.append(
                            RecipeWithMatch(
                                **recipe.dict(),
                                matchingCount=0,
                                matchingIngredients=[]
                            )
                        )

                process_time = time.time() - start_time
                logger.info(f"Text search completed in {process_time:.3f}s: {len(results)} results")

                return RecipeSearchResponse(
                    recipes=results,
                    count=len(results),
                    query=body.query,
                    search_method="vector"
                )

            except Exception as e:
                logger.warning(f"Vector search failed: {e}, falling back to string matching")
                # Fall through to string matching

        # Fallback: Simple string matching in recipe titles
        logger.info(f"Text search request: '{body.query}', method: string_matching")
        recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())

        query_lower = body.query.lower()
        results = []

        for recipe in recipes:
            if query_lower in recipe.Title.lower():
                results.append(
                    RecipeWithMatch(
                        **recipe.dict(),
                        matchingCount=0,
                        matchingIngredients=[]
                    )
                )
                if len(results) >= top_k:
                    break

        process_time = time.time() - start_time
        logger.info(f"Text search completed in {process_time:.3f}s: {len(results)} results")

        return RecipeSearchResponse(
            recipes=results,
            count=len(results),
            query=body.query,
            search_method="string_matching"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in text search: {e}")
        raise HTTPException(status_code=500, detail=f"Tarif araması başarısız: {str(e)}")


@router.post("/rag-recommend", response_model=RAGRecommendResponse)
@limiter.limit("20/minute")
async def rag_recommend(
    request: Request,
    body: RAGRecommendRequest,
    user: Optional[dict] = Depends(get_optional_user),
):
    """
    RAG-based recipe recommendations with personalization.

    Complete pipeline: Retrieve (FAISS) → Rerank → Personalize → Generate (Gemini LLM)
    Personalization is applied when the request comes from a logged-in user.
    """
    start_time = time.time()

    try:
        if not body.ingredients:
            raise HTTPException(status_code=400, detail="Malzeme listesi gerekli")

        preferences_dict = None
        if body.preferences:
            preferences_dict = {
                "vegan": body.preferences.vegan or False,
                "vegetarian": body.preferences.vegetarian or False,
                "glutenFree": body.preferences.glutenFree or False,
                "dairyFree": body.preferences.dairyFree or False,
                "nutAllergy": body.preferences.nutAllergy or False,
            }

        top_k = body.top_k if body.top_k is not None else 10
        retrieval_top_k = body.retrieval_top_k if body.retrieval_top_k is not None else 50
        explain = body.explain if body.explain is not None else True

        # Fetch interaction history + CF scores for logged-in users
        user_history: Optional[dict] = None
        user_id: Optional[str] = None
        cf_scores: Optional[dict] = None
        if user:
            user_id = user["id"]
            try:
                user_history = await database_service.get_user_interaction_map(user_id)
                logger.info(
                    f"[{user['email']}] RAG personalized: {len(user_history)} known recipes"
                )
            except Exception as exc:
                logger.warning(f"Could not fetch user history for personalization: {exc}")

            try:
                all_titles = [r.Title for r in recipe_service.get_all_recipes(
                    limit=recipe_service.get_total_count()
                )]
                cf_scores = await cf_service.get_cf_scores(user_id, all_titles)
                if cf_scores:
                    logger.info(f"[{user['email']}] CF: {len(cf_scores)} tarife skor eklendi")
            except Exception as exc:
                logger.warning(f"CF skorları hesaplanamadı: {exc}")

        logger.info(
            f"RAG recommendation: {len(body.ingredients)} ingredients, "
            f"top_k={top_k}, explain={explain}, personalized={bool(user_history)}"
        )

        result = rag_pipeline.process(
            user_ingredients=body.ingredients,
            user_preferences=preferences_dict,
            excluded_ingredients=body.excluded_ingredients or [],
            top_k=top_k,
            explain=explain,
            retrieval_top_k=retrieval_top_k,
            user_id=user_id,
            user_history=user_history,
            cf_scores=cf_scores,
        )

        process_time = time.time() - start_time
        logger.info(
            f"RAG pipeline completed in {process_time:.3f}s: "
            f"{len(result['recipes'])} recipes, "
            f"explanation={'yes' if result['explanation'] else 'no'}"
        )

        return RAGRecommendResponse(
            recipes=result["recipes"],
            explanation=result["explanation"],
            metadata=result["metadata"],
            count=len(result["recipes"]),
            match_score=result.get("match_score"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in RAG recommendation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"RAG önerileri oluşturulamadı: {str(e)}"
        )


@router.post("/substitutions", response_model=SubstitutionResponse)
@limiter.limit("10/minute")
async def get_substitutions(request: Request, body: SubstitutionRequest):
    """
    Get ingredient substitution suggestions via LLM.

    Accepts a recipe title, a list of missing ingredients, and the user's
    available ingredients. Returns per-ingredient substitution options.
    """
    try:
        if not body.missing_ingredients:
            return SubstitutionResponse(substitutions={}, explanation=None)

        logger.info(
            f"Substitution request: '{body.recipe_title}', "
            f"{len(body.missing_ingredients)} missing ingredients"
        )

        result = llm_service.generate_substitutions(
            recipe_title=body.recipe_title,
            missing_ingredients=body.missing_ingredients,
            available_ingredients=body.available_ingredients,
        )

        if result is None:
            raise HTTPException(
                status_code=503,
                detail="LLM servisi şu anda kullanılamıyor. Lütfen daha sonra tekrar deneyin."
            )

        subs = result.get("substitutions", {})
        if not isinstance(subs, dict):
            subs = {}
        return SubstitutionResponse(
            substitutions=subs,
            explanation=result.get("explanation"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error generating substitutions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"İkame önerileri oluşturulamadı: {str(e)}"
        )

