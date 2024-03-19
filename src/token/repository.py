from dataclasses import dataclass
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.exceptions import TokenDontExist
from src.token.models import TokenModel


@dataclass
class TokenRepository:
    session: AsyncSession

    async def find_token(self, jwt_token: str):
        """Поиск токена"""
        token = await self.session.execute(Select(TokenModel).filter(TokenModel.token == jwt_token))
        if not token:
            raise TokenDontExist
        return token.scalar()
