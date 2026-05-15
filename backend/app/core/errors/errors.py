import typing as tp

from starlette import status


class AppException(Exception):
    def __init__(
            self,
            error_key: str,
            error_message: str,
            status_code: int,
            error_loc: tp.Optional[tp.Sequence[str]] = None
    ):
        self.error_key = error_key
        self.error_message = error_message
        self.status_code = status_code
        self.error_loc = error_loc
        super().__init__()


class OAuthHttpException(AppException):
    def __init__(
            self,
            error_key: str = "oauth.invalid_grant",
            error_message: str = "Code is expired.",
            status_code: int = status.HTTP_400_BAD_REQUEST,
            error_loc: tp.Optional[tp.Sequence[str]] = None,
    ):
        super().__init__(error_key, error_message, status_code, error_loc)


class ForbiddenException(AppException):
    def __init__(
            self,
            error_key: str = "forbidden",
            error_message: str = "Forbidden",
            status_code: int = status.HTTP_403_FORBIDDEN,
            error_loc: tp.Optional[tp.Sequence[str]] = None
    ) -> None:
        super().__init__(error_key, error_message, status_code, error_loc)


class JWTTokenException(AppException):
    def __init__(
            self,
            error_key: str = "authorization.invalid",
            error_message: str = "Invalid authorization token",
            status_code: int = status.HTTP_401_UNAUTHORIZED,
            error_loc: tp.Optional[tp.Sequence[str]] = ("header", "Authorization"),
    ):
        super().__init__(error_key, error_message, status_code, error_loc)
