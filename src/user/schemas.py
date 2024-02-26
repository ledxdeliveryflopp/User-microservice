from pydantic import BaseModel


class UserBaseSchemas(BaseModel):
    """Базовая схема пользователя"""

    username: str
    email: str
