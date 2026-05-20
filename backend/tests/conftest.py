"""Pytest fixtures — shared test client and auth helpers."""
import os
import asyncio
import pytest

# Prevent tests from sending real e-mail; expose dev_token in magic-link response
os.environ.setdefault("SESSION_SECRET", "test-secret-key-for-pytest")
os.environ["SMTP_ENABLED"] = "false"

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db, engine


async def _setup_db():
    await init_db()
    # Dispose all pooled connections created during init so that each test's
    # function-scoped event loop gets clean connections (no cross-loop errors).
    await engine.dispose()


asyncio.run(_setup_db())


@pytest.fixture(autouse=True)
async def _dispose_after_each():
    """Dispose pooled DB connections after every test to prevent cross-loop errors."""
    yield
    await engine.dispose()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac


# Convenience: authenticated client (session cookie already set)
@pytest.fixture
async def auth_client(client):
    """Returns (client, user_email) with a valid session cookie."""
    import uuid
    email = f"test-{uuid.uuid4().hex[:12]}@example.com"
    r1 = await client.post("/api/auth/magic-link", json={"email": email})
    assert r1.status_code == 200, r1.text
    token = r1.json()["dev_token"]
    r2 = await client.post("/api/auth/verify", json={"token": token})
    assert r2.status_code == 200, r2.text
    yield client, email
