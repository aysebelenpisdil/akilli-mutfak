"""Feedback endpoint testleri — auth gerekli, UPSERT ve toggle mantığı."""

# ── Auth guard ────────────────────────────────────────────────────────────────

async def test_interaction_requires_auth(client):
    r = await client.post(
        "/api/feedback/interaction",
        json={"recipe_title": "Karnıyarık", "interaction_type": "like"},
    )
    assert r.status_code == 401


async def test_consumption_requires_auth(client):
    r = await client.post(
        "/api/feedback/consumption",
        json={"recipe_title": "Karnıyarık", "meal_type": "dinner", "portion_size": 1.0},
    )
    assert r.status_code == 401


async def test_features_requires_auth(client):
    r = await client.get("/api/feedback/features")
    assert r.status_code == 401


async def test_history_requires_auth(client):
    r = await client.get("/api/feedback/history")
    assert r.status_code == 401


async def test_recipe_status_requires_auth(client):
    r = await client.get("/api/feedback/recipe-status/Karnıyarık")
    assert r.status_code == 401


# ── Full flow ─────────────────────────────────────────────────────────────────

async def test_feedback_flow_with_auth(auth_client):
    client, _ = auth_client

    # Like a recipe
    r = await client.post(
        "/api/feedback/interaction",
        json={
            "recipe_title": "Karnıyarık",
            "interaction_type": "like",
            "context_ingredients": ["patlıcan", "kıyma"],
        },
    )
    assert r.status_code == 200
    like_id = r.json()["id"]
    assert like_id > 0

    # Log consumption
    r = await client.post(
        "/api/feedback/consumption",
        json={"recipe_title": "Karnıyarık", "meal_type": "dinner", "portion_size": 1.5},
    )
    assert r.status_code == 200

    # Features reflect the interaction
    r = await client.get("/api/feedback/features")
    assert r.status_code == 200
    data = r.json()
    assert data["total_likes"] >= 1


async def test_like_is_idempotent_upsert(auth_client):
    """Liking the same recipe 3× must result in exactly 1 row, not 3."""
    client, _ = auth_client
    recipe = "Upsert Test Tarifi"

    ids = []
    for _ in range(3):
        r = await client.post(
            "/api/feedback/interaction",
            json={"recipe_title": recipe, "interaction_type": "like"},
        )
        assert r.status_code == 200
        ids.append(r.json()["id"])

    # All calls return the same row id (UPSERT behaviour)
    assert len(set(ids)) == 1, f"Expected single row id, got {ids}"

    # History must contain exactly 1 like for this recipe
    r = await client.get("/api/feedback/history?limit=200")
    assert r.status_code == 200
    likes = [
        i for i in r.json()["interactions"]
        if i["recipe_title"] == recipe and i["interaction_type"] == "like"
    ]
    assert len(likes) == 1, f"Expected 1 row, got {len(likes)}"


async def test_toggle_like_unlike(auth_client):
    """Like then unlike → no record remains."""
    client, _ = auth_client
    recipe = "Toggle Test Tarifi"

    # Like
    r = await client.post(
        "/api/feedback/interaction",
        json={"recipe_title": recipe, "interaction_type": "like"},
    )
    assert r.status_code == 200

    # Unlike (DELETE by recipe+type)
    import json as _json
    r = await client.request(
        "DELETE",
        "/api/feedback/interaction",
        content=_json.dumps({"recipe_title": recipe, "interaction_type": "like"}),
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
    assert r.json()["deleted"] == 1

    # Recipe status must be null now
    r = await client.get(f"/api/feedback/recipe-status/{recipe}")
    assert r.status_code == 200
    assert r.json()["status"] is None


async def test_recipe_status_tracks_last_interaction(auth_client):
    """After like→skip the status must be 'skip'."""
    client, _ = auth_client
    recipe = "Status Track Tarifi"

    await client.post(
        "/api/feedback/interaction",
        json={"recipe_title": recipe, "interaction_type": "like"},
    )
    await client.post(
        "/api/feedback/interaction",
        json={"recipe_title": recipe, "interaction_type": "skip"},
    )

    r = await client.get(f"/api/feedback/recipe-status/{recipe}")
    assert r.status_code == 200
    # Should reflect most recent: skip
    assert r.json()["status"] == "skip"


async def test_interaction_history_pagination(auth_client):
    """History endpoint respects limit/offset."""
    client, _ = auth_client

    r = await client.get("/api/feedback/history?limit=5&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert "interactions" in data
    assert "count" in data
    assert len(data["interactions"]) <= 5


async def test_delete_nonexistent_interaction_returns_zero(auth_client):
    """Deleting a recipe that was never liked returns deleted=0, not an error."""
    import json as _json
    client, _ = auth_client
    r = await client.request(
        "DELETE",
        "/api/feedback/interaction",
        content=_json.dumps({"recipe_title": "Hiç Beğenilmemiş Tarif", "interaction_type": "like"}),
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 200
    assert r.json()["deleted"] == 0
