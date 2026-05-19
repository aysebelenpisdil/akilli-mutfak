"""Fridge endpoint testleri — full-overwrite persistence."""


async def test_fridge_requires_auth(client):
    r = await client.get("/api/fridge/ingredients")
    assert r.status_code == 401


async def test_fridge_save_requires_auth(client):
    r = await client.post("/api/fridge/ingredients", json={"ingredients": ["domates"]})
    assert r.status_code == 401


async def test_fridge_get_initially_empty(auth_client):
    """Fresh user has no fridge ingredients beyond what other tests may have added."""
    client, _ = auth_client
    r = await client.get("/api/fridge/ingredients")
    assert r.status_code == 200
    assert "ingredients" in r.json()


async def test_fridge_save_and_retrieve(auth_client):
    client, _ = auth_client
    ingredients = ["domates", "biber", "soğan"]

    r = await client.post("/api/fridge/ingredients", json={"ingredients": ingredients})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True

    r = await client.get("/api/fridge/ingredients")
    assert r.status_code == 200
    saved = r.json()["ingredients"]
    assert set(saved) == set(ingredients)


async def test_fridge_full_overwrite(auth_client):
    """Second POST replaces first completely — no merge."""
    client, _ = auth_client

    await client.post("/api/fridge/ingredients", json={"ingredients": ["elma", "armut"]})
    await client.post("/api/fridge/ingredients", json={"ingredients": ["portakal"]})

    r = await client.get("/api/fridge/ingredients")
    saved = r.json()["ingredients"]
    assert "portakal" in saved
    assert "elma" not in saved
    assert "armut" not in saved


async def test_fridge_empty_save(auth_client):
    """Saving an empty list clears the fridge."""
    client, _ = auth_client

    await client.post("/api/fridge/ingredients", json={"ingredients": ["sarımsak"]})
    await client.post("/api/fridge/ingredients", json={"ingredients": []})

    r = await client.get("/api/fridge/ingredients")
    assert r.json()["ingredients"] == []


async def test_fridge_strips_blank_ingredients(auth_client):
    """Blank/whitespace-only strings must not be persisted."""
    client, _ = auth_client

    r = await client.post("/api/fridge/ingredients", json={"ingredients": ["domates", "", "  "]})
    assert r.status_code == 200

    r = await client.get("/api/fridge/ingredients")
    saved = r.json()["ingredients"]
    assert "" not in saved
    assert "  " not in saved
    assert "domates" in saved
