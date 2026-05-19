"""Auth (magic link, session, logout) endpoint testleri."""


async def test_magic_link_request(client):
    r = await client.post("/api/auth/magic-link", json={"email": "test@example.com"})
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "dev_token" in data  # SMTP_ENABLED=false → token açık gelir


async def test_magic_link_invalid_email(client):
    r = await client.post("/api/auth/magic-link", json={"email": "gecersiz"})
    assert r.status_code == 422


async def test_magic_link_missing_email_field(client):
    r = await client.post("/api/auth/magic-link", json={})
    assert r.status_code == 422


async def test_verify_magic_link(client):
    r1 = await client.post("/api/auth/magic-link", json={"email": "verify-test@example.com"})
    assert r1.status_code == 200
    token = r1.json().get("dev_token")
    assert token

    r2 = await client.post("/api/auth/verify", json={"token": token})
    assert r2.status_code == 200
    data = r2.json()
    assert data["user"]["email"] == "verify-test@example.com"
    # Session cookie must be set
    assert "session_id" in r2.cookies or "Set-Cookie" in str(r2.headers)


async def test_me_requires_auth(client):
    r = await client.get("/api/auth/me")
    assert r.status_code == 401


async def test_me_after_login(client):
    r1 = await client.post("/api/auth/magic-link", json={"email": "me-test@example.com"})
    token = r1.json()["dev_token"]
    await client.post("/api/auth/verify", json={"token": token})

    r = await client.get("/api/auth/me")
    assert r.status_code == 200
    assert r.json()["user"]["email"] == "me-test@example.com"


async def test_logout_clears_session(client):
    r1 = await client.post("/api/auth/magic-link", json={"email": "logout-test@example.com"})
    token = r1.json()["dev_token"]
    await client.post("/api/auth/verify", json={"token": token})

    # Confirm logged in
    assert (await client.get("/api/auth/me")).status_code == 200

    # Logout
    r = await client.post("/api/auth/logout")
    assert r.status_code in (200, 204)

    # Must be 401 now
    r = await client.get("/api/auth/me")
    assert r.status_code == 401


async def test_invalid_token_rejected(client):
    r = await client.post("/api/auth/verify", json={"token": "not-a-real-token"})
    assert r.status_code in (400, 401, 422)


async def test_token_cannot_be_reused(client):
    """Magic link token is single-use; second verify must fail."""
    r1 = await client.post("/api/auth/magic-link", json={"email": "reuse-test@example.com"})
    token = r1.json()["dev_token"]

    r2 = await client.post("/api/auth/verify", json={"token": token})
    assert r2.status_code == 200

    r3 = await client.post("/api/auth/verify", json={"token": token})
    assert r3.status_code in (400, 401, 422)
