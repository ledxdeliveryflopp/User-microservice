from dataclasses import dataclass
from datetime import datetime
from jose import jwt
from starlette.requests import Request
from src.settings.exceptions import TokenDontExist, TokenExpire
from src.settings.service import SessionService
from src.settings.settings import settings
from src.token.repository import TokenRepository


@dataclass
class TokenService:
    _token_repository: TokenRepository
    _session_service: SessionService
    request: Request

    async def verify_token(self):
        """Проверка токена на существование и срок действия"""
        header_token = self.request.headers.get('Authorization')
        header_token = header_token.replace("Bearer ", "")
        token = await self._token_repository.find_token(jwt_token=header_token)
        if not token:
            raise TokenDontExist
        date = datetime.utcnow()
        if token.expire < date:
            await self._session_service.delete_object(delete_object=token)
            raise TokenExpire
        return token

    async def get_token_payload(self):
        """Email и роль пользователя из токена"""
        token = await self.verify_token()
        if not token:
            raise TokenDontExist
        token = token.token
        token_payload = jwt.decode(token=token, key=settings.jwt_settings.jwt_secret,
                                   algorithms=settings.jwt_settings.jwt_algorithm)
        user_email = token_payload.get("user_email")
        user_role = token_payload.get("user_role")
        return {"user_email": user_email, "user_role": user_role}
