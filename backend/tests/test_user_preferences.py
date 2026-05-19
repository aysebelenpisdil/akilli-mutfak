"""User preferences endpoint testleri."""


async def test_preferences_requires_auth(client):
    r = await client.get("/api/user/preferences")
    assert r.status_code == 401


async def test_save_preferences_requires_auth(client):
    r = await client.post("/api/user/preferences", json={"dietary": {}, "excluded": []})
    assert r.status_code == 401


async def test_preferences_default_empty(auth_client):
    client, _ = auth_client
    r = await client.get("/api/user/preferences")
    assert r.status_code == 200
    data = r.json()
    assert "dietary" in data
    assert "excluded" in data


async def test_save_and_retrieve_preferences(auth_client):
    client, _ = auth_client

    payload = {
        "dietary": {"vegan": True, "glutenFree": False, "vegetarian": False, "dairyFree": True, "nutAllergy": False},
        "excluded": ["fıstık", "fındık"],
    }
    r = await client.post("/api/user/preferences", json=payload)
    assert r.status_code == 200

    r = await client.get("/api/user/preferences")
    assert r.status_code == 200
    data = r.json()
    assert data["dietary"].get("vegan") is True
    assert data["dietary"].get("dairyFree") is True
    assert "fıstık" in data["excluded"]
    assert "fındık" in data["excluded"]


async def test_preferences_overwrite(auth_client):
    """Second save replaces dietary/excluded completely."""
    client, _ = auth_client

    await client.post("/api/user/preferences", json={
        "dietary": {"vegan": True}, "excluded": ["elma"]
    })
    await client.post("/api/user/preferences", json={
        "dietary": {"vegan": False, "glutenFree": True}, "excluded": []
    })

    r = await client.get("/api/user/preferences")
    data = r.json()
    assert data["dietary"].get("vegan") is False
    assert data["dietary"].get("glutenFree") is True
    assert data["excluded"] == []
