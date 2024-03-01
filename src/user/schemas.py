from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBaseSchemas(BaseModel):
    """Базовая схема пользователя"""

    username: str
    email: EmailStr


class UserUpdateSchemas(BaseModel):
    """Схема обновления пользователя"""

    username: Optional[str] = None
    email:  Optional[EmailStr] = None
