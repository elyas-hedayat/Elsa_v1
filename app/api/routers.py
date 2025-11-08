from fastapi import APIRouter

from app.core.redis_client import redis_client

router = APIRouter()


@router.get("/cache-test")
def cache_test():
    redis_client.set("test_key", "Hello Redis!")
    value = redis_client.get("test_key")
    return {"stored_value": value}
