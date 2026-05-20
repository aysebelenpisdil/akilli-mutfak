from __future__ import annotations

import json
import logging
from datetime import datetime
from sqlalchemy import text
from app.database import engine, init_db as _init_db

logger = logging.getLogger(__name__)


def _as_str(val):
    return val.isoformat() if isinstance(val, datetime) else val


class DatabaseService:

    async def init_db(self):
        await _init_db()

    async def record_interaction(self, user_id: str, recipe_title: str,
                                  interaction_type: str,
                                  context_ingredients: list[str] | None = None) -> int:
        ctx_json = json.dumps(context_ingredients, ensure_ascii=False) if context_ingredients else None
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""INSERT INTO recipe_interactions
                        (user_id, recipe_title, interaction_type, context_ingredients)
                        VALUES (:user_id, :recipe_title, :interaction_type, :ctx)
                        ON CONFLICT (user_id, recipe_title, interaction_type)
                            WHERE interaction_type IN ('like','skip','save','cook')
                            DO UPDATE SET
                                created_at = NOW(),
                                context_ingredients = EXCLUDED.context_ingredients
                        RETURNING id"""),
                {"user_id": user_id, "recipe_title": recipe_title,
                 "interaction_type": interaction_type, "ctx": ctx_json},
            )
            row = result.fetchone()
            return row[0]

    async def delete_interaction_by_recipe(self, user_id: str, recipe_title: str,
                                            interaction_type: str) -> int:
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""DELETE FROM recipe_interactions
                        WHERE user_id = :user_id
                          AND recipe_title = :recipe_title
                          AND interaction_type = :interaction_type"""),
                {"user_id": user_id, "recipe_title": recipe_title,
                 "interaction_type": interaction_type},
            )
            return result.rowcount

    async def log_consumption(self, user_id: str, recipe_title: str,
                               meal_type: str, portion_size: float = 1.0,
                               rating: int | None = None,
                               notes: str | None = None) -> int:
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""INSERT INTO consumption_logs
                        (user_id, recipe_title, meal_type, portion_size, rating, notes)
                        VALUES (:user_id, :recipe_title, :meal_type, :portion_size, :rating, :notes)
                        RETURNING id"""),
                {"user_id": user_id, "recipe_title": recipe_title, "meal_type": meal_type,
                 "portion_size": portion_size, "rating": rating, "notes": notes},
            )
            row = result.fetchone()
            return row[0]

    async def _query_weekly_repeats(self, conn, user_id: str) -> list[str]:
        result = await conn.execute(
            text("""SELECT recipe_title FROM consumption_logs
                    WHERE user_id = :user_id
                      AND consumed_at >= NOW() - INTERVAL '7 days'
                    GROUP BY recipe_title HAVING COUNT(*) >= 2"""),
            {"user_id": user_id},
        )
        return [r[0] for r in result.fetchall()]

    async def get_user_features(self, user_id: str) -> dict:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT * FROM user_features WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            row = result.mappings().fetchone()
            if not row:
                return {
                    "user_id": user_id, "email": "", "total_likes": 0,
                    "total_skips": 0, "total_cooked": 0, "avg_portion": None,
                    "preferred_meal_type": None, "weekly_repeat_count": 0,
                    "like_skip_ratio": None, "top_liked_recipes": [],
                    "weekly_repeats": [],
                }

            features = dict(row)

            total_likes = features.get("total_likes", 0)
            total_skips = features.get("total_skips", 0)
            features["like_skip_ratio"] = (
                round(total_likes / total_skips, 2)
                if total_skips > 0 else None
            )

            result = await conn.execute(
                text("""SELECT recipe_title, COUNT(*) AS cnt
                        FROM recipe_interactions
                        WHERE user_id = :user_id AND interaction_type = 'like'
                        GROUP BY recipe_title ORDER BY cnt DESC LIMIT 10"""),
                {"user_id": user_id},
            )
            features["top_liked_recipes"] = [r[0] for r in result.fetchall()]
            features["weekly_repeats"] = await self._query_weekly_repeats(conn, user_id)
            return features

    async def get_weekly_repeats(self, user_id: str) -> list[str]:
        async with engine.connect() as conn:
            return await self._query_weekly_repeats(conn, user_id)

    async def get_interaction_history(self, user_id: str,
                                       limit: int = 50, offset: int = 0) -> list[dict]:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""SELECT id, recipe_title, interaction_type, created_at
                        FROM recipe_interactions
                        WHERE user_id = :user_id
                        ORDER BY created_at DESC LIMIT :limit OFFSET :offset"""),
                {"user_id": user_id, "limit": limit, "offset": offset},
            )
            return [
                {k: _as_str(v) for k, v in dict(r._mapping).items()}
                for r in result.fetchall()
            ]

    async def get_consumption_history(self, user_id: str,
                                       limit: int = 50, offset: int = 0) -> list[dict]:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""SELECT id, recipe_title, consumed_at, meal_type, portion_size, rating, notes
                        FROM consumption_logs
                        WHERE user_id = :user_id
                        ORDER BY consumed_at DESC LIMIT :limit OFFSET :offset"""),
                {"user_id": user_id, "limit": limit, "offset": offset},
            )
            return [
                {k: _as_str(v) for k, v in dict(r._mapping).items()}
                for r in result.fetchall()
            ]

    async def get_recipe_interaction_status(self, user_id: str, recipe_title: str) -> dict:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""SELECT interaction_type FROM recipe_interactions
                        WHERE user_id = :user_id AND recipe_title = :recipe_title
                          AND interaction_type IN ('like', 'skip')
                        ORDER BY created_at DESC LIMIT 1"""),
                {"user_id": user_id, "recipe_title": recipe_title},
            )
            row = result.fetchone()
            return {"status": row[0] if row else None}

    async def delete_interaction(self, user_id: str, interaction_id: int) -> bool:
        async with engine.begin() as conn:
            result = await conn.execute(
                text("DELETE FROM recipe_interactions WHERE id = :id AND user_id = :user_id"),
                {"id": interaction_id, "user_id": user_id},
            )
            return result.rowcount > 0

    async def get_user_interaction_map(self, user_id: str) -> dict[str, str]:
        """Return {recipe_title: most_recent_interaction_type} for the given user."""
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT DISTINCT ON (recipe_title) recipe_title, interaction_type
                    FROM recipe_interactions
                    WHERE user_id = :user_id
                    ORDER BY recipe_title, created_at DESC
                """),
                {"user_id": user_id},
            )
            return {row[0]: row[1] for row in result.fetchall()}

    async def get_fridge_ingredients(self, user_id: str) -> list[str]:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT ingredient FROM fridge_ingredients WHERE user_id = :user_id ORDER BY ingredient"),
                {"user_id": user_id},
            )
            return [r[0] for r in result.fetchall()]

    async def save_fridge_ingredients(self, user_id: str, ingredients: list[str]) -> None:
        async with engine.begin() as conn:
            await conn.execute(
                text("DELETE FROM fridge_ingredients WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            for ing in ingredients:
                if ing and str(ing).strip():
                    await conn.execute(
                        text("""INSERT INTO fridge_ingredients (user_id, ingredient)
                                VALUES (:user_id, :ingredient)
                                ON CONFLICT DO NOTHING"""),
                        {"user_id": user_id, "ingredient": str(ing).strip()},
                    )


    async def get_shopping_list(self, user_id: str) -> list[dict]:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""SELECT item_name, display_name, purchased, from_recipes
                        FROM shopping_list_items
                        WHERE user_id = :user_id
                        ORDER BY purchased, created_at"""),
                {"user_id": user_id},
            )
            items = []
            for r in result.fetchall():
                items.append({
                    "name": r[0],
                    "display_name": r[1],
                    "purchased": bool(r[2]),
                    "from_recipes": json.loads(r[3]) if r[3] else [],
                })
            return items

    async def save_shopping_list(self, user_id: str, items: list[dict]) -> None:
        async with engine.begin() as conn:
            await conn.execute(
                text("DELETE FROM shopping_list_items WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            for it in items:
                name = (it.get("name") or "").strip().lower()
                if not name:
                    continue
                await conn.execute(
                    text("""INSERT INTO shopping_list_items
                            (user_id, item_name, display_name, purchased, from_recipes)
                            VALUES (:user_id, :name, :display, :purchased, :recipes)
                            ON CONFLICT (user_id, item_name) DO UPDATE SET
                                display_name = EXCLUDED.display_name,
                                purchased = EXCLUDED.purchased,
                                from_recipes = EXCLUDED.from_recipes"""),
                    {
                        "user_id": user_id,
                        "name": name,
                        "display": it.get("display_name", name),
                        "purchased": 1 if it.get("purchased") else 0,
                        "recipes": json.dumps(it.get("from_recipes", []), ensure_ascii=False) or None,
                    },
                )

    async def get_user_preferences(self, user_id: str) -> dict:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT dietary_preferences, excluded_ingredients FROM users WHERE id = :id"),
                {"id": user_id},
            )
            row = result.mappings().fetchone()
            if not row:
                return {"dietary": {}, "excluded": []}
            return {
                "dietary": json.loads(row["dietary_preferences"]) if row["dietary_preferences"] else {},
                "excluded": json.loads(row["excluded_ingredients"]) if row["excluded_ingredients"] else [],
            }

    async def save_user_preferences(self, user_id: str, dietary: dict, excluded: list) -> None:
        async with engine.begin() as conn:
            await conn.execute(
                text("UPDATE users SET dietary_preferences = :d, excluded_ingredients = :e WHERE id = :id"),
                {"d": json.dumps(dietary), "e": json.dumps(excluded), "id": user_id},
            )


    async def record_survey_response(
        self,
        user_id: str,
        rating: int,
        cook_intent: str,
        comment: str | None,
        context_ingredients: list[str] | None,
        recipe_titles: list[str] | None,
    ) -> tuple[int, str]:
        ctx = json.dumps(context_ingredients, ensure_ascii=False) if context_ingredients else None
        titles = json.dumps(recipe_titles, ensure_ascii=False) if recipe_titles else None
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""INSERT INTO survey_responses
                        (user_id, rating, cook_intent, comment, context_ingredients, recipe_titles)
                        VALUES (:user_id, :rating, :cook_intent, :comment, :ctx, :titles)
                        RETURNING id, created_at"""),
                {
                    "user_id": user_id, "rating": rating, "cook_intent": cook_intent,
                    "comment": comment, "ctx": ctx, "titles": titles,
                },
            )
            row = result.fetchone()
            return row[0], _as_str(row[1])

    async def get_survey_stats(self) -> dict:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT COUNT(*), COALESCE(AVG(rating::float), 0) FROM survey_responses")
            )
            row = result.fetchone()
            total = int(row[0])
            avg_rating = round(float(row[1]), 2)

            result = await conn.execute(
                text("SELECT cook_intent, COUNT(*) FROM survey_responses GROUP BY cook_intent")
            )
            cook_breakdown: dict = {"yes": 0, "maybe": 0, "no": 0}
            for r in result.fetchall():
                cook_breakdown[r[0]] = int(r[1])

            result = await conn.execute(
                text("SELECT rating, COUNT(*) FROM survey_responses GROUP BY rating ORDER BY rating")
            )
            rating_dist: dict = {str(i): 0 for i in range(1, 6)}
            for r in result.fetchall():
                rating_dist[str(r[0])] = int(r[1])

            return {
                "total_responses": total,
                "average_rating": avg_rating,
                "cook_intent_breakdown": cook_breakdown,
                "rating_distribution": rating_dist,
            }


database_service = DatabaseService()
