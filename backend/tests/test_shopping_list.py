"""Shopping list endpoint testleri — persistence, idempotency, auth guard."""


# ── Auth guards ───────────────────────────────────────────────────────────────

async def test_shopping_list_get_requires_auth(client):
    r = await client.get("/api/shopping-list/items")
    assert r.status_code == 401


async def test_shopping_list_post_requires_auth(client):
    r = await client.post("/api/shopping-list/items", json={"items": []})
    assert r.status_code == 401


# ── Basic CRUD ────────────────────────────────────────────────────────────────

async def test_shopping_list_initially_accessible(auth_client):
    client, _ = auth_client
    r = await client.get("/api/shopping-list/items")
    assert r.status_code == 200
    assert "items" in r.json()


async def test_shopping_list_save_and_retrieve(auth_client):
    client, _ = auth_client
    items = [
        {"name": "patlican", "display_name": "Patlıcan", "purchased": False, "from_recipes": ["İmam Bayıldı"]},
        {"name": "sogangn", "display_name": "Soğan", "purchased": False, "from_recipes": []},
    ]

    r = await client.post("/api/shopping-list/items", json={"items": items})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["count"] == 2

    r = await client.get("/api/shopping-list/items")
    saved = r.json()["items"]
    names = {i["name"] for i in saved}
    assert "patlican" in names
    assert "sogangn" in names


async def test_shopping_list_full_overwrite(auth_client):
    """Second POST replaces everything — mirrors fridge behaviour."""
    client, _ = auth_client

    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "elma", "display_name": "Elma", "purchased": False, "from_recipes": []}]
    })
    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "portakal", "display_name": "Portakal", "purchased": False, "from_recipes": []}]
    })

    r = await client.get("/api/shopping-list/items")
    saved_names = {i["name"] for i in r.json()["items"]}
    assert "portakal" in saved_names
    assert "elma" not in saved_names


async def test_shopping_list_purchased_flag_persisted(auth_client):
    client, _ = auth_client

    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "seker", "display_name": "Şeker", "purchased": True, "from_recipes": []}]
    })

    r = await client.get("/api/shopping-list/items")
    item = next(i for i in r.json()["items"] if i["name"] == "seker")
    assert item["purchased"] is True


async def test_shopping_list_from_recipes_persisted(auth_client):
    """from_recipes JSON array must round-trip correctly."""
    client, _ = auth_client

    recipes = ["Hünkar Beğendi", "İmam Bayıldı"]
    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "patlican2", "display_name": "Patlıcan", "purchased": False, "from_recipes": recipes}]
    })

    r = await client.get("/api/shopping-list/items")
    item = next(i for i in r.json()["items"] if i["name"] == "patlican2")
    assert set(item["from_recipes"]) == set(recipes)


async def test_shopping_list_empty_save_clears(auth_client):
    client, _ = auth_client

    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "tuz", "display_name": "Tuz", "purchased": False, "from_recipes": []}]
    })
    await client.post("/api/shopping-list/items", json={"items": []})

    r = await client.get("/api/shopping-list/items")
    assert r.json()["items"] == []


async def test_shopping_list_blank_name_ignored(auth_client):
    """Items with blank name must be silently dropped."""
    client, _ = auth_client

    await client.post("/api/shopping-list/items", json={
        "items": [
            {"name": "  ", "display_name": "Blank", "purchased": False, "from_recipes": []},
            {"name": "biber", "display_name": "Biber", "purchased": False, "from_recipes": []},
        ]
    })

    r = await client.get("/api/shopping-list/items")
    names = {i["name"] for i in r.json()["items"]}
    assert "biber" in names
    assert "" not in names
    assert "  " not in names


async def test_shopping_list_item_name_normalized_lowercase(auth_client):
    """item_name is stored lowercase regardless of input case."""
    client, _ = auth_client

    await client.post("/api/shopping-list/items", json={
        "items": [{"name": "DOMATES", "display_name": "Domates", "purchased": False, "from_recipes": []}]
    })

    r = await client.get("/api/shopping-list/items")
    names = [i["name"] for i in r.json()["items"]]
    assert "domates" in names
    assert "DOMATES" not in names
