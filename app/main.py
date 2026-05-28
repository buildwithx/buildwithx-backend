from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.db.indexes import create_indexes
from app.db.mongo import database
from app.features.auth.router import router as auth_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_indexes(database)

    yield


app = FastAPI(title=settings.app_name)

register_exception_handlers(app)


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(
    auth_router,
    prefix=settings.api_prefix,
)
