"""
Content-based baseline recommender using Jaccard similarity over ingredients.
Corresponds to the "basit içerik tabanlı baseline önerici" required by the thesis proposal.
"""

import ast
import json
import logging
from typing import List, Set, Tuple

logger = logging.getLogger(__name__)


def _parse_ingredient_list(raw: str) -> List[str]:
    """Parse a cleaned_ingredients string (Python repr or JSON array)."""
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return [str(x).strip().lower() for x in parsed]
    except Exception:
        pass
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(x).strip().lower() for x in parsed]
    except Exception:
        pass
    # Fallback: treat whole string as single ingredient
    return [raw.strip().lower()]


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


class JaccardRecommender:
    """
    Recommends recipes by Jaccard similarity between the query ingredient set
    and each recipe's cleaned_ingredients set.
    Lazy-loads the recipe catalog on first call.
    """

    def __init__(self):
        self._catalog: List[Tuple[str, Set[str]]] = []  # (title, ingredient_set)

    def _ensure_loaded(self) -> None:
        if self._catalog:
            return
        # Import here to avoid circular deps at module load time
        from app.services.recipe_service import recipe_service
        recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())
        self._catalog = [
            (r.Title, set(_parse_ingredient_list(r.Cleaned_Ingredients)))
            for r in recipes
        ]
        logger.debug(f"JaccardRecommender: loaded {len(self._catalog)} recipes")

    def recommend(self, query_ingredients: List[str], top_k: int = 10) -> List[str]:
        self._ensure_loaded()
        query_set = {ing.strip().lower() for ing in query_ingredients}
        scored = [
            (title, _jaccard(query_set, ing_set))
            for title, ing_set in self._catalog
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [title for title, _ in scored[:top_k]]


# Module-level singleton reused across evaluation runs
jaccard_recommender = JaccardRecommender()
