from fastapi import APIRouter, Depends, status

from app.features.auth.dependencies import (
    get_auth_service,
    get_current_user,
)
from app.features.auth.schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
    UserRead,
)
from app.features.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth Controller"])


@router.post(
    "/register",
    response_model=TokenPair,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    return await service.register(payload)


@router.post(
    "/login",
    response_model=TokenPair,
)
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    return await service.login(payload)


@router.post(
    "/refresh",
    response_model=TokenPair,
)
async def refresh(
    payload: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    return await service.refresh(payload.refresh_token)


@router.get(
    "/me",
    response_model=UserRead,
)
async def me(
    current_user: dict = Depends(get_current_user),
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: LogoutRequest,
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.logout(payload.refresh_token)
