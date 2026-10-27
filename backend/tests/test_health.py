def test_health(client):
    r=client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["service"] == "PPE Guard API"

def test_model_contract_metadata(client):
    data=client.get("/api/v1/models").json()
    assert data["class_count"] == 12
    assert data["classes"]["6"] == "head"
    assert data["classes"]["10"] == "none"
