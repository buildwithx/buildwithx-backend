from typing import Any
from datetime import timedelta
from redis.asyncio import Redis

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.features.auth.models import UserDocument

from app.core.security import hash_token


class AuthRepository:
    def __init__(
        self,
        database: AsyncIOMotorDatabase[Any],
        redis: Redis,
    ) -> None:
        self.collection = database["users"]
        self.redis = redis

    # ---------------------------------
    # User handling
    # ---------------------------------

    # get user by email
    async def get_user_by_email(
        self,
        email: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one({"email": email})

    # get user by username
    async def get_user_by_username(
        self,
        username: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one({"username": username})

    # get user by ID
    async def get_user_by_id(
        self,
        user_id: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": user_id})

    # create a new user
    async def create_user(
        self,
        user: UserDocument,
    ) -> dict[str, Any]:
        payload = user.model_dump(
            by_alias=True,
            exclude={"id"},
        )

        result = await self.collection.insert_one(payload)

        created_user = await self.collection.find_one(
            {"_id": result.inserted_id},
        )

        if created_user is None:
            raise RuntimeError("User creation failed: document not found after insert")

        return created_user

    # ----------------------------
    # Refresh token handling
    # ----------------------------
    async def store_refresh_token(
        self,
        *,
        user_id: str,
        refresh_token: str,
        expires_in_days: int,
    ) -> None:
        token_hash = hash_token(refresh_token)

        await self.redis.set(
            f"refresh:{token_hash}",
            user_id,
            ex=timedelta(days=expires_in_days),
        )

    async def validate_refresh_token(
        self,
        refresh_token: str,
    ) -> bool:
        token_hash = hash_token(refresh_token)

        token = await self.redis.get(f"refresh:{token_hash}")

        return token is not None

    async def revoke_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        token_hash = hash_token(refresh_token)

        await self.redis.delete(f"refresh:{token_hash}")
