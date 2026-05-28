from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.features.auth.dependencies import get_auth_service
from app.features.auth.service import AuthService
from app.main import app


class FakeRepository:
    def __init__(self):
        self.users: list[dict] = []
        self.refresh_tokens: dict[str, str] = {}

    async def get_user_by_email(self, email: str) -> dict | None:
        for user in self.users:
            if user["email"] == email:
                return user
        return None

    async def get_user_by_username(self, username: str) -> dict | None:
        for user in self.users:
            if user["username"] == username:
                return user
        return None

    async def get_user_by_id(self, user_id: str) -> dict | None:
        for user in self.users:
            if user["_id"] == user_id:
                return user
        return None

    async def create_user(self, user) -> dict:
        import bson

        new_user = {
            "_id": bson.ObjectId(),
            "email": user.email,
            "username": user.username,
            "password_hash": user.password_hash,
            "role": "reader",
            "created_at": bson.datetime.datetime.now(),
        }
        self.users.append(new_user)
        return new_user

    async def store_refresh_token(
        self,
        *,
        user_id: str,
        refresh_token: str,
        expires_in_days: int,
    ) -> None:
        self.refresh_tokens[refresh_token] = user_id

    async def validate_refresh_token(self, refresh_token: str) -> bool:
        return refresh_token in self.refresh_tokens

    async def revoke_refresh_token(self, refresh_token: str) -> None:
        self.refresh_tokens.pop(refresh_token, None)


@pytest.fixture
def fake_repository():
    return FakeRepository()


@pytest.fixture
def auth_service(fake_repository):
    return AuthService(fake_repository)


@pytest.fixture
async def api_client(auth_service) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_service():
        return auth_service

    app.dependency_overrides[get_auth_service] = override_get_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.pop(get_auth_service, None)
