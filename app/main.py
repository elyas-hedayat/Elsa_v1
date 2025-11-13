from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.api.routers import router
from app.api.routes.auth_router import router as auth_router
from app.api.routes.user_route import router as user_router
from app.core.config import settings
from app.core.databases import engine, init_db

sentry_sdk.init(
    dsn=settings.sentry_dns,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,
    environment=settings.app_env,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)
Instrumentator().instrument(app).expose(app)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0  # noqa
