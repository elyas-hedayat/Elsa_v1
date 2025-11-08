from fastapi.testclient import TestClient
from starlette import status

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "redis_url" in data


def test_health_redis():
    response = client.get("cache-test")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["stored_value"] == "Hello Redis!"
