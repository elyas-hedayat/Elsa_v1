from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from starlette import status

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"


@patch("app.api.routers.redis_client", new_callable=MagicMock)
def test_health_redis(mock_redis_client):
    mock_redis_client.get.return_value = "Hello Redis!"
    response = client.get("/cache-test")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["stored_value"] == "Hello Redis!"
    mock_redis_client.set.assert_called_with("test_key", "Hello Redis!")
    mock_redis_client.get.assert_called_with("test_key")
