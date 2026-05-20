from __future__ import annotations

import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.config import settings

logger = logging.getLogger(__name__)

# Convert generic postgresql:// URL to the asyncpg dialect
_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1).split("?")[0]

engine = create_async_engine(
    _url,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        # Disable client-side prepared statement cache.
        # With statement_cache_size=0, asyncpg uses unnamed (transient) prepared
        # statements that are safe with PgBouncer in transaction pooling mode.
        # Named statements (via prepared_statement_name_func) persist across the
        # pool's backend connections and cause "does not exist" errors under pgbouncer.
        "statement_cache_size": 0,
    },
)

_SCHEMA_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        display_name TEXT,
        dietary_preferences TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login_at TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS magic_links (
        id BIGSERIAL PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        is_active INTEGER DEFAULT 1
    )""",
    """CREATE TABLE IF NOT EXISTS recipe_interactions (
        id BIGSERIAL PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        recipe_title TEXT NOT NULL,
        interaction_type TEXT NOT NULL CHECK(interaction_type IN ('like','skip','view','cook','save')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        context_ingredients TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS consumption_logs (
        id BIGSERIAL PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        recipe_title TEXT NOT NULL,
        consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        meal_type TEXT CHECK(meal_type IN ('breakfast','lunch','dinner','snack')),
        portion_size REAL DEFAULT 1.0,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        notes TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS fridge_ingredients (
        user_id TEXT NOT NULL REFERENCES users(id),
        ingredient TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, ingredient)
    )""",
    """CREATE TABLE IF NOT EXISTS shopping_list_items (
        id BIGSERIAL PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        item_name TEXT NOT NULL,
        display_name TEXT NOT NULL,
        purchased INTEGER DEFAULT 0,
        from_recipes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, item_name)
    )""",
    """CREATE TABLE IF NOT EXISTS survey_responses (
        id BIGSERIAL PRIMARY KEY,
        user_id TEXT NOT NULL REFERENCES users(id),
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        cook_intent TEXT NOT NULL CHECK(cook_intent IN ('yes','maybe','no')),
        comment TEXT,
        context_ingredients TEXT,
        recipe_titles TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    "CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_magic_links_token ON magic_links(token)",
    "CREATE INDEX IF NOT EXISTS idx_interactions_user ON recipe_interactions(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_interactions_type ON recipe_interactions(interaction_type)",
    "CREATE INDEX IF NOT EXISTS idx_interactions_recipe ON recipe_interactions(recipe_title)",
    "CREATE INDEX IF NOT EXISTS idx_consumption_user ON consumption_logs(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_consumption_date ON consumption_logs(consumed_at)",
    "CREATE INDEX IF NOT EXISTS idx_fridge_user ON fridge_ingredients(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_shopping_list_user ON shopping_list_items(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_survey_user ON survey_responses(user_id)",
    # Prevent duplicate like/skip/save/cook per user+recipe (view is exempt — it's a log)
    # Note: one-time duplicate cleanup was performed in May 2026; no longer needed at startup.
    """CREATE UNIQUE INDEX IF NOT EXISTS uniq_interaction_per_user_recipe_type
       ON recipe_interactions(user_id, recipe_title, interaction_type)
       WHERE interaction_type IN ('like','skip','save','cook')""",
]

_VIEW_SQL = """
CREATE OR REPLACE VIEW user_features AS
SELECT
    u.id AS user_id,
    u.email,
    COUNT(DISTINCT CASE WHEN ri.interaction_type = 'like' THEN ri.recipe_title END) AS total_likes,
    COUNT(DISTINCT CASE WHEN ri.interaction_type = 'skip' THEN ri.recipe_title END) AS total_skips,
    COUNT(DISTINCT CASE WHEN ri.interaction_type = 'cook' THEN ri.recipe_title END) AS total_cooked,
    AVG(cl.portion_size) AS avg_portion,
    (SELECT meal_type FROM consumption_logs
     WHERE user_id = u.id
     GROUP BY meal_type ORDER BY COUNT(*) DESC LIMIT 1) AS preferred_meal_type,
    (SELECT COUNT(*) FROM (
        SELECT recipe_title FROM consumption_logs
        WHERE user_id = u.id
          AND consumed_at >= NOW() - INTERVAL '7 days'
        GROUP BY recipe_title HAVING COUNT(*) >= 2
    ) sub) AS weekly_repeat_count
FROM users u
LEFT JOIN recipe_interactions ri ON u.id = ri.user_id
LEFT JOIN consumption_logs cl ON u.id = cl.user_id
GROUP BY u.id, u.email
"""


async def init_db() -> None:
    async with engine.begin() as conn:
        for stmt in _SCHEMA_STATEMENTS:
            await conn.execute(text(stmt))
        await conn.execute(text(_VIEW_SQL))
        await conn.execute(text(
            "ALTER TABLE users DROP COLUMN IF EXISTS password_hash"
        ))
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS excluded_ingredients TEXT"
        ))
    logger.info("PostgreSQL schema initialized on Supabase")
