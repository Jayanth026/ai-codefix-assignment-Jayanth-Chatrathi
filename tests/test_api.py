from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_local_fix_schema():
    payload = {
        "language": "java",
        "cwe": "CWE-89",
        "code": 'String query = "SELECT * FROM users WHERE id=" + userId;'
    }
    response = client.post("/local_fix", json=payload)
    assert response.status_code == 200
    data = response.json()
    for key in ["fixed_code", "diff", "explanation", "model_used", "token_usage", "latency_ms"]:
        assert key in data
