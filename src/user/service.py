from dataclasses import dataclass
from src.user.repository import UserRepository
from src.user.schemas import UserUpdateSchemas


@dataclass
class UserService:
    repository: UserRepository

    async def get_all_users(self):
        users = await self.repository.get_all_users()
        return users

    async def get_user_by_email(self, email: str):
        user = await self.repository.get_user_by_email(email=email)
        return user

    async def get_current_user(self):
        user = await self.repository.get_current_user()
        return user

    async def update_user(self, user_schemas_update: UserUpdateSchemas):
        user = await self.repository.update_user(user_schemas_update=user_schemas_update)
        return user

    async def delete_user(self):
        user = await self.repository.delete_user()
        return user
