from typing import Any
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class TokenDontExist(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Token don't exist."


class TokenExpire(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Token date expire."


class EmptyAuthorizationHeader(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Empty authorization header."


class UserDontExist(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User don't exist."
