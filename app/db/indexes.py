from typing import Any
from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_indexes(
    database: AsyncIOMotorDatabase[Any],
) -> None:
    await database["users"].create_index(
        "email",
        unique=True,
    )

    await database["users"].create_index(
        "username",
        unique=True,
    )

    await database["articles"].create_index(
        [("slug", 1)],
        unique=True,
    )

    await database["articles"].create_index(
        [("status", 1), ("published_at", -1)],
    )

    await database["articles"].create_index(
        [("author_id", 1), ("published_at", -1)],
    )

    await database["articles"].create_index(
        [("tags", 1), ("published_at", -1)],
    )

    await database["articles"].create_index(
        [("title", "text"), ("subtitle", "text"), ("content", "text")],
    )
