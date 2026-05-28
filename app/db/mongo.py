from typing import Any

from collections.abc import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

settings = get_settings()

client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(settings.mongo_uri)
database: AsyncIOMotorDatabase[Any] = client[settings.mongo_database]


async def get_database() -> AsyncIterator[AsyncIOMotorDatabase]:
    yield database
