"""Survey endpoint testleri."""

async def test_survey_requires_auth(client):
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 4, "cook_intent": "yes"},
    )
    assert r.status_code == 401


async def test_survey_stats_requires_auth(client):
    r = await client.get("/api/feedback/survey/stats")
    assert r.status_code == 401


async def test_submit_survey_success(auth_client):
    client, email = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={
            "rating": 4,
            "cook_intent": "yes",
            "comment": "Çok iyi öneriler",
            "context_ingredients": ["domates", "soğan"],
            "recipe_titles": ["Menemen", "Omlet"],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] > 0
    assert "created_at" in data


async def test_submit_survey_minimal(auth_client):
    client, _ = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 3, "cook_intent": "maybe"},
    )
    assert r.status_code == 200
    assert r.json()["id"] > 0


async def test_submit_survey_invalid_rating_zero(auth_client):
    client, _ = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 0, "cook_intent": "yes"},
    )
    assert r.status_code == 422


async def test_submit_survey_invalid_rating_six(auth_client):
    client, _ = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 6, "cook_intent": "yes"},
    )
    assert r.status_code == 422


async def test_submit_survey_invalid_intent(auth_client):
    client, _ = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 3, "cook_intent": "maybeee"},
    )
    assert r.status_code == 422


async def test_submit_survey_comment_too_long(auth_client):
    client, _ = auth_client
    r = await client.post(
        "/api/feedback/survey",
        json={"rating": 2, "cook_intent": "no", "comment": "a" * 501},
    )
    assert r.status_code == 422


async def test_get_survey_stats(auth_client):
    client, _ = auth_client

    # Submit 3 responses so stats are non-trivial
    payloads = [
        {"rating": 5, "cook_intent": "yes"},
        {"rating": 3, "cook_intent": "maybe"},
        {"rating": 1, "cook_intent": "no"},
    ]
    for p in payloads:
        r = await client.post("/api/feedback/survey", json=p)
        assert r.status_code == 200

    r = await client.get("/api/feedback/survey/stats")
    assert r.status_code == 200
    data = r.json()

    assert data["total_responses"] >= 3
    assert 1.0 <= data["average_rating"] <= 5.0
    assert "yes" in data["cook_intent_breakdown"]
    assert "maybe" in data["cook_intent_breakdown"]
    assert "no" in data["cook_intent_breakdown"]
    assert "1" in data["rating_distribution"]
    assert "5" in data["rating_distribution"]
