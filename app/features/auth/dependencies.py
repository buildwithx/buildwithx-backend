import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

from app.core.security import TokenType, decode_token
from app.db.mongo import get_database
from app.db.redis import get_redis
from app.features.auth.exceptions import InvalidToken, ForbiddenError
from app.features.auth.repository import AuthRepository
from app.features.auth.service import AuthService

bearer_scheme = HTTPBearer()


async def get_auth_service(
    database: AsyncIOMotorDatabase = Depends(get_database),
    redis: Redis = Depends(get_redis),
) -> AuthService:
    repository = AuthRepository(database, redis)

    return AuthService(repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme,
    ),
    database: AsyncIOMotorDatabase = Depends(get_database),
    redis: Redis = Depends(get_redis),
) -> dict:
    try:
        payload = decode_token(credentials.credentials)
    except jwt.InvalidTokenError as error:
        raise InvalidToken() from error

    if payload.get("type") != TokenType.ACCESS:
        raise InvalidToken()

    repository = AuthRepository(database, redis)

    user = await repository.get_user_by_email(payload["sub"])

    if not user:
        raise InvalidToken()

    return user


# Role-Based Authorization
# * Usage
# ```@router.post("/articles")
#       async def create_article(
#           current_user: dict = Depends(require_role("author")),
#       ):
#           pass
# ```


def require_role(role: str):
    async def dependency(
        current_user: dict = Depends(get_current_user),
    ) -> dict:
        if current_user["role"] != role:
            raise ForbiddenError()

        return current_user

    return dependency
