from fastapi import FastAPI

from app.api.routers import router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "redis_url": settings.redis_url,
    }
