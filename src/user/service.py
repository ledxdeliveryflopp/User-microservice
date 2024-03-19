from dataclasses import dataclass
from src.settings.exceptions import UserDontExist
from src.settings.service import SessionService
from src.token.service import TokenService
from src.user.repository import UserRepository
from src.user.schemas import UserUpdateSchemas


@dataclass
class UserService:
    _user_repository: UserRepository
    _token_service: TokenService
    _session_service: SessionService

    async def get_all_users(self):
        return await self._user_repository.get_all_users()

    async def get_user_by_email(self, email: str):
        user = await self._user_repository.get_user_by_email(email=email)
        return user

    async def get_current_user(self):
        """Получить пользователя из токена"""
        token = await self._token_service.get_token_payload()
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
        await self._session_service.save_update_object(save_object=user)
        return user

    async def delete_user(self):
        """Удалить пользователя"""
        user = await self.get_current_user()
        if not user:
            raise UserDontExist
        await self._session_service.delete_object(delete_object=user)
        return {"detail": "success"}
