"""
Test query builders for offline evaluation.

Two strategies:
  build_synthetic_queries  — hold out 20% of recipes; sample 3-5 ingredients as query.
  fetch_interaction_queries (async) — leave-one-out on real user like/cook interactions.
"""

import ast
import json
import logging
import random
from typing import List, Set, Tuple

logger = logging.getLogger(__name__)

# (query_ingredients, relevant_recipe_titles)
QuerySet = List[Tuple[List[str], Set[str]]]


def _parse_ingredient_list(raw: str) -> List[str]:
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
    return [raw.strip().lower()]


def build_synthetic_queries(
    seed: int = 42,
    holdout_ratio: float = 0.2,
    sample_min: int = 3,
    sample_max: int = 5,
) -> QuerySet:
    """
    Hold out holdout_ratio of the recipe catalog as the test set.
    For each held-out recipe, randomly sample sample_min..sample_max of its
    cleaned ingredients as the query; the recipe itself is the only ground-truth.
    Recipes with fewer than sample_min ingredients are skipped.
    """
    from app.services.recipe_service import recipe_service

    recipe_service._ensure_loaded()
    all_recipes = recipe_service.get_all_recipes(limit=recipe_service.get_total_count())

    rng = random.Random(seed)
    shuffled = list(all_recipes)
    rng.shuffle(shuffled)

    n_test = max(1, int(len(shuffled) * holdout_ratio))
    test_recipes = shuffled[:n_test]

    queries: QuerySet = []
    skipped = 0
    for recipe in test_recipes:
        ingredients = _parse_ingredient_list(recipe.Cleaned_Ingredients)
        if len(ingredients) < sample_min:
            skipped += 1
            continue
        n_sample = min(rng.randint(sample_min, sample_max), len(ingredients))
        sampled = rng.sample(ingredients, n_sample)
        queries.append((sampled, {recipe.Title}))

    logger.info(
        f"build_synthetic_queries: {len(queries)} queries built "
        f"(seed={seed}, holdout={holdout_ratio}, {skipped} skipped)"
    )
    return queries


async def fetch_interaction_queries(min_interactions: int = 3) -> QuerySet:
    """
    Leave-one-out evaluation using real user interactions.
    For each user with >= min_interactions like/cook events (with context_ingredients),
    hold out the most recent one; query = context_ingredients, ground-truth = recipe.
    """
    from app.database import engine
    from sqlalchemy import text

    queries: QuerySet = []

    async with engine.connect() as conn:
        result = await conn.execute(
            text("""
                SELECT user_id, COUNT(*) AS cnt
                FROM recipe_interactions
                WHERE interaction_type IN ('like', 'cook')
                  AND context_ingredients IS NOT NULL
                GROUP BY user_id
                HAVING COUNT(*) >= :min_int
            """),
            {"min_int": min_interactions},
        )
        users = [row[0] for row in result.fetchall()]

        for user_id in users:
            result = await conn.execute(
                text("""
                    SELECT recipe_title, context_ingredients
                    FROM recipe_interactions
                    WHERE user_id = :user_id
                      AND interaction_type IN ('like', 'cook')
                      AND context_ingredients IS NOT NULL
                    ORDER BY created_at DESC
                    LIMIT 1
                """),
                {"user_id": user_id},
            )
            row = result.fetchone()
            if not row:
                continue
            recipe_title, ctx_json = row
            try:
                query_ingredients = json.loads(ctx_json)
            except Exception:
                continue
            if not query_ingredients:
                continue
            queries.append((query_ingredients, {recipe_title}))

    logger.info(f"fetch_interaction_queries: {len(queries)} queries from {len(users)} users")
    return queries
