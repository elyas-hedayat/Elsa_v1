from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text

from app.core.databases import get_session
from app.core.redis_client import redis_client

router = APIRouter()


@router.get("/cache-test")
def cache_test():
    redis_client.set("test_key", "Hello Redis!")
    value = redis_client.get("test_key")
    return {"stored_value": value}


@router.get("/db-test")
async def db_test(
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    result = await session.execute(text("SELECT 1"))
    return {"result": result.scalar()}
