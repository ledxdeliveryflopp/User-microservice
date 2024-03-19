from dataclasses import dataclass
from sqlalchemy import Select
from starlette.requests import Request
from src.settings.exceptions import UserDontExist, UsersDontExist, BadRole
from src.settings.repository import SessionRepository
from src.token.repository import TokenRepository
from src.user.models import UserModel, Role
from src.user.schemas import UserUpdateSchemas


@dataclass
class UserRepository:
    session_repository: SessionRepository
    token_repository: TokenRepository
    request: Request

    async def get_all_users(self):
        """Получить всех пользователей"""
        token_data = await self.token_repository.get_token_payload()
        token_role = token_data.get("user_role")
        if token_role != Role.admin:
            raise BadRole
        users = await self.session_repository.session.execute(Select(UserModel))
        if not users:
            raise UsersDontExist
        return users.scalars().all()

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session_repository.session.execute(Select(UserModel)
                                                             .filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

    async def get_current_user(self):
        """Получить пользователя из токена"""
        token = await self.token_repository.get_token_payload()
        token_data = token.get("user_email")
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
        await self.session_repository.save_update_object(save_object=user)
        return user

    async def delete_user(self):
        """Удалить пользователя"""
        user = await self.get_current_user()
        if not user:
            raise UserDontExist
        await self.session_repository.delete_object(delete_object=user)
        return {"detail": "success"}
