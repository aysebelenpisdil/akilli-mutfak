from __future__ import annotations

import uuid
import logging
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import text
from app.config import settings
from app.database import engine

logger = logging.getLogger(__name__)

serializer = URLSafeTimedSerializer(settings.SESSION_SECRET)


def _as_str(val):
    return val.isoformat() if isinstance(val, datetime) else val


class AuthService:

    async def create_or_get_user(self, email: str) -> dict:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT id, email, display_name, created_at FROM users WHERE email = :email"),
                {"email": email},
            )
            row = result.mappings().fetchone()
            if row:
                return {k: _as_str(v) for k, v in dict(row).items()}

        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        async with engine.begin() as conn:
            await conn.execute(
                text("INSERT INTO users (id, email, created_at) VALUES (:id, :email, :created_at)"),
                {"id": user_id, "email": email, "created_at": now},
            )
        return {"id": user_id, "email": email, "display_name": None, "created_at": _as_str(now)}

    async def generate_magic_link(self, user_id: str) -> str:
        token = serializer.dumps(user_id, salt="magic-link")
        expires_at = datetime.utcnow() + timedelta(seconds=settings.MAGIC_LINK_EXPIRY)

        async with engine.begin() as conn:
            await conn.execute(
                text("INSERT INTO magic_links (user_id, token, expires_at) VALUES (:user_id, :token, :expires_at)"),
                {"user_id": user_id, "token": token, "expires_at": expires_at},
            )

        logger.info(f"Magic link generated for user {user_id}")
        return token

    async def verify_magic_link(self, token: str) -> dict | None:
        try:
            user_id = serializer.loads(token, salt="magic-link", max_age=settings.MAGIC_LINK_EXPIRY)
        except Exception:
            logger.warning("Invalid or expired magic link token")
            return None

        async with engine.begin() as conn:
            result = await conn.execute(
                text("SELECT id, user_id FROM magic_links WHERE token = :token AND used = 0"),
                {"token": token},
            )
            link = result.mappings().fetchone()
            if not link:
                return None

            await conn.execute(
                text("UPDATE magic_links SET used = 1 WHERE id = :id"),
                {"id": link["id"]},
            )

            now = datetime.utcnow()
            await conn.execute(
                text("UPDATE users SET last_login_at = :now WHERE id = :id"),
                {"now": now, "id": user_id},
            )

            result = await conn.execute(
                text("SELECT id, email, display_name, created_at FROM users WHERE id = :id"),
                {"id": user_id},
            )
            user = result.mappings().fetchone()
            return {k: _as_str(v) for k, v in dict(user).items()} if user else None

    async def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRY_DAYS)

        async with engine.begin() as conn:
            await conn.execute(
                text("INSERT INTO sessions (id, user_id, expires_at) VALUES (:id, :user_id, :expires_at)"),
                {"id": session_id, "user_id": user_id, "expires_at": expires_at},
            )

        return session_id

    async def validate_session(self, session_id: str) -> dict | None:
        if not session_id:
            return None

        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT s.id AS session_id, s.expires_at, s.is_active,
                           u.id AS user_id, u.email, u.display_name, u.created_at
                    FROM sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.id = :session_id AND s.is_active = 1
                """),
                {"session_id": session_id},
            )
            row = result.mappings().fetchone()
            if not row:
                return None

            expires_at = row["expires_at"]
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            if expires_at < datetime.utcnow():
                async with engine.begin() as wconn:
                    await wconn.execute(
                        text("UPDATE sessions SET is_active = 0 WHERE id = :id"),
                        {"id": session_id},
                    )
                return None

            return {
                "id": row["user_id"],
                "email": row["email"],
                "display_name": row["display_name"],
                "created_at": _as_str(row["created_at"]),
                "session_expires_at": _as_str(row["expires_at"]),
            }

    async def logout(self, session_id: str):
        async with engine.begin() as conn:
            await conn.execute(
                text("UPDATE sessions SET is_active = 0 WHERE id = :id"),
                {"id": session_id},
            )


auth_service = AuthService()
