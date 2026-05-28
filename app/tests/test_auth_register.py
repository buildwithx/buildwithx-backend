import pytest
from httpx import AsyncClient

from app.features.auth.schemas import RegisterRequest


@pytest.mark.asyncio
async def test_register_success(api_client: AsyncClient):
    payload = RegisterRequest(
        email="test@example.com",
        password="securepassword123",
    )

    response = await api_client.post(
        "/api/v1/auth/register",
        json=payload.model_dump(),
    )

    assert response.status_code == 201

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(api_client: AsyncClient):
    payload = RegisterRequest(
        email="duplicate@example.com",
        password="securepassword123",
    )

    await api_client.post(
        "/api/v1/auth/register",
        json=payload.model_dump(),
    )

    response = await api_client.post(
        "/api/v1/auth/register",
        json=payload.model_dump(),
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_invalid_email(api_client: AsyncClient):
    response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "not-an-email",
            "password": "securepassword123",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(api_client: AsyncClient):
    response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422
