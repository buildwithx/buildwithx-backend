from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from app.core.exceptions import AppError


class InvalidCredentials(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            status_code=HTTP_401_UNAUTHORIZED,
        )


class UserAlreadyExists(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message="User already exists",
            status_code=HTTP_400_BAD_REQUEST,
        )


class InvalidToken(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_TOKEN",
            message="Invalid or expired token",
            status_code=HTTP_401_UNAUTHORIZED,
        )


class ForbiddenError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="FORBIDDEN",
            message="You do not have permission",
            status_code=HTTP_403_FORBIDDEN,
        )
