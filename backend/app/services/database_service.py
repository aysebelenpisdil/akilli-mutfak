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
                        RETURNING id"""),
                {"user_id": user_id, "recipe_title": recipe_title,
                 "interaction_type": interaction_type, "ctx": ctx_json},
            )
            row = result.fetchone()
            return row[0]

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


database_service = DatabaseService()
