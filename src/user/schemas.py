from pydantic import BaseModel, EmailStr


class UserBaseSchemas(BaseModel):
    """Базовая схема пользователя"""

    username: str
    email: EmailStr


class UserUpdateSchemas(BaseModel):
    """Схема обновления пользователя"""
    username: str
