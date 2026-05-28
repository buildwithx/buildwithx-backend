import jwt

from app.shared.username_generator import UsernameGenerator

from app.core.security import (
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.features.auth.exceptions import (
    InvalidCredentials,
    InvalidToken,
    UserAlreadyExists,
)
from app.features.auth.models import UserDocument
from app.features.auth.repository import AuthRepository
from app.features.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenPair,
)

from app.core.config import get_settings

settings = get_settings()


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    async def _generate_unique_username(self) -> str:
        while True:
            username = UsernameGenerator.generate()

            existing_user = await self.repository.get_user_by_username(
                username,
            )

            if not existing_user:
                return username

    # Register
    async def register(
        self,
        payload: RegisterRequest,
    ) -> TokenPair:
        existing_user = await self.repository.get_user_by_email(
            payload.email,
        )

        if existing_user:
            raise UserAlreadyExists()

        username = await self._generate_unique_username()

        user = UserDocument(
            email=payload.email,
            username=username,
            password_hash=hash_password(payload.password),
        )

        created_user = await self.repository.create_user(user)

        access_token = create_access_token(created_user["email"])
        refresh_token = create_refresh_token(created_user["email"])

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    # Login
    async def login(
        self,
        payload: LoginRequest,
    ) -> TokenPair:
        user = await self.repository.get_user_by_email(payload.email)

        if not user:
            raise InvalidCredentials()

        is_valid_password = verify_password(
            payload.password,
            user["password_hash"],
        )

        if not is_valid_password:
            raise InvalidCredentials()

        access_token = create_access_token(user["email"])
        refresh_token = create_refresh_token(user["email"])

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    # Refresh token
    async def refresh(
        self,
        refresh_token: str,
    ) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except jwt.InvalidTokenError as error:
            raise InvalidToken() from error

        if payload.get("type") != TokenType.REFRESH:
            raise InvalidToken()

        is_valid = await self.repository.validate_refresh_token(
            refresh_token,
        )

        if not is_valid:
            raise InvalidToken()

        subject = payload["sub"]

        await self.repository.revoke_refresh_token(
            refresh_token,
        )

        new_access_token = create_access_token(subject)
        new_refresh_token = create_refresh_token(subject)

        await self.repository.store_refresh_token(
            user_id=subject,
            refresh_token=new_refresh_token,
            expires_in_days=settings.refresh_token_expire_days,
        )

        return TokenPair(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def logout(
        self,
        refresh_token: str,
    ) -> None:
        await self.repository.revoke_refresh_token(refresh_token)
