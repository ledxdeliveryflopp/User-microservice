from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.exceptions import UserDontExist
from src.token.service import get_token_payload
from src.user.models import UserModel


async def get_all_users(session: AsyncSession):
    """Получить всех пользователей"""
    users = await session.execute(Select(UserModel))
    return users.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str):
    user = await session.execute(Select(UserModel).filter(UserModel.email == email))
    if not user:
        raise UserDontExist
    return user.scalar()


async def get_current_user(session: AsyncSession, request: Request):
    token_data = await get_token_payload(session=session,  request=request)
    user = await get_user_by_email(session=session, email=token_data)
    if not user:
        raise UserDontExist
    return user

