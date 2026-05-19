"""Health ve root endpoint testleri."""


async def test_health_ok(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "database" in data
    assert data["database"]["available"] is True
    assert "PostgreSQL" in data["database"]["type"]


async def test_health_includes_rag_pipeline(client):
    r = await client.get("/health")
    data = r.json()
    assert "rag_pipeline" in data
    assert "retriever" in data["rag_pipeline"]
    assert "reranker" in data["rag_pipeline"]
    assert "generator" in data["rag_pipeline"]


async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
