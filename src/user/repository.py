from dataclasses import dataclass
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.exceptions import UserDontExist
from src.settings.repository import SessionRepository
# from src.token.service import get_token_payload
from src.token.repository import TokenRepository
from src.token.service import TokenService
from src.user.models import UserModel
from src.user.schemas import UserUpdateSchemas


@dataclass
class UserRepository:
    session: AsyncSession
    request: Request

    async def get_all_users(self):
        """Получить всех пользователей"""
        users = await self.session.execute(Select(UserModel))
        return users.scalars().all()

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

    async def get_current_user(self):
        """Получить пользователя из токена"""
        token_repository = TokenRepository(request=self.request, session=self.session)
        token_data = await token_repository.get_token_payload()
        user = await self.get_user_by_email(email=token_data)
        if not user:
            raise UserDontExist
        return user

    async def update_user(self, user_schemas_update: UserUpdateSchemas):
        """Обновить пользователя"""
        user = await self.get_current_user()
        if not user:
            raise UserDontExist
        for key, value in vars(user_schemas_update).items():
            setattr(user, key, value) if value else None
        session_update = SessionRepository(session=self.session, object=user)
        await session_update.save_update_object()
        return user

    async def delete_user(self):
        """Удалить пользователя"""
        user = await self.get_current_user()
        if not user:
            raise UserDontExist
        session_delete = SessionRepository(session=self.session, object=user)
        await session_delete.delete_object()
        return {"detail": "success"}
