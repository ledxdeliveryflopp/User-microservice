from dataclasses import dataclass
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.exceptions import UserDontExist, UsersDontExist, BadRole
from src.token.service import TokenService
from src.user.models import UserModel, Role


@dataclass
class UserRepository:
    session: AsyncSession
    _token_service: TokenService

    async def get_all_users(self):
        """Получить всех пользователей"""
        token_data = await self._token_service.get_token_payload()
        token_role = token_data.get("user_role")
        if token_role != Role.admin:
            raise BadRole
        users = await self.session.execute(Select(UserModel))
        if not users:
            raise UsersDontExist
        return users.scalars().all()

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

