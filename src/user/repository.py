from dataclasses import dataclass
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.exceptions import UserDontExist, UsersDontExist
from src.user.models import UserModel


@dataclass
class UserRepository:
    session: AsyncSession

    async def get_all_users(self, limit: int, offset: int):
        """Получить всех пользователей"""
        users = await self.session.execute(Select(UserModel).limit(limit).offset(offset))
        if not users:
            raise UsersDontExist
        return users.scalars().all()

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

