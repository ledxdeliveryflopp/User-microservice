from dataclasses import dataclass
from jose import jwt
from starlette.requests import Request
from src.settings.exceptions import TokenDontExist
from src.settings.service import SessionService
from src.settings.settings import settings
from src.token.repository import TokenRepository


@dataclass
class TokenService:
    """Сервис токенов"""
    _token_repository: TokenRepository
    _session_service: SessionService
    request: Request

    async def get_token_payload(self) -> dict:
        """Email и роль пользователя из токена"""
        header_token = self.request.headers.get('Authorization')
        header_token = header_token.replace("Bearer ", "")
        token = await self._token_repository.find_token(jwt_token=header_token)
        if not token:
            raise TokenDontExist
        token = token.token
        token_payload = jwt.decode(token=token, key=settings.jwt_settings.jwt_secret,
                                   algorithms=settings.jwt_settings.jwt_algorithm)
        user_email = token_payload.get("user_email")
        return {'email': user_email}
