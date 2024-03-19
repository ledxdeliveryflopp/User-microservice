from dataclasses import dataclass
from datetime import datetime
from jose import jwt
from sqlalchemy import Select
from starlette.requests import Request
from src.settings.exceptions import TokenDontExist
from src.settings.repository import SessionRepository
from src.settings.settings import settings
from src.token.models import TokenModel


@dataclass
class TokenRepository:
    session_repository: SessionRepository
    request: Request

    async def find_token(self, jwt_token: str):
        """Поиск токена"""
        token = await self.session_repository.session.execute(Select(TokenModel)
                                                              .filter(TokenModel.token == jwt_token))
        if not token:
            raise TokenDontExist
        return token.scalar()

    async def verify_token(self):
        """Проверка токена на существование и срок действия"""
        header_token = self.request.headers.get('Authorization')
        header_token = header_token.replace("Bearer ", "")
        token = await self.find_token(jwt_token=header_token)
        if not token:
            raise TokenDontExist
        date = datetime.utcnow()
        if token.expire < date:
            await self.session_repository.delete_object(delete_object=token)
        return token

    async def get_token_payload(self):
        """Email пользователя из токена"""
        token = await self.verify_token()
        if not token:
            raise TokenDontExist
        token = token.token
        token_payload = jwt.decode(token=token, key=settings.jwt_settings.jwt_secret,
                                   algorithms=settings.jwt_settings.jwt_algorithm)
        user_email = token_payload.get("user_email")
        user_role = token_payload.get("user_role")
        return {"user_email": user_email, "user_role": user_role}
