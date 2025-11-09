import sentry_sdk
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.api.routers import router
from app.core.config import settings

sentry_sdk.init(
    dsn=settings.sentry_dns,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,
    environment=settings.app_env,
)


app = FastAPI(title=settings.app_name)
app.include_router(router)
Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
        "redis_url": settings.redis_url,
    }


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0  # noqa
