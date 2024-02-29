from pydantic import BaseModel, EmailStr


class UserBaseSchemas(BaseModel):
    """Базовая схема пользователя"""

    username: str
    email: EmailStr


class UserUpdateSchemas(UserBaseSchemas):
    """Схема обновления пользователя"""

    pass
