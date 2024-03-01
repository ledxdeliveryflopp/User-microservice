from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.exceptions import UserDontExist
from src.token.service import get_token_payload
from src.user.models import UserModel
from src.user.schemas import UserUpdateSchemas


async def get_all_users(session: AsyncSession):
    """Получить всех пользователей"""
    users = await session.execute(Select(UserModel))
    return users.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str):
    """Получить пользователя по Email"""
    user = await session.execute(Select(UserModel).filter(UserModel.email == email))
    if not user:
        raise UserDontExist
    return user.scalar()


async def get_current_user(session: AsyncSession, request: Request):
    """Получить пользователя из токена"""
    token_data = await get_token_payload(session=session,  request=request)
    user = await get_user_by_email(session=session, email=token_data)
    if not user:
        raise UserDontExist
    return user


async def update_user(session: AsyncSession, user_schemas_update: UserUpdateSchemas,
                      request: Request):
    """Обновить пользователя"""
    user = await get_current_user(session=session, request=request)
    if not user:
        raise UserDontExist
    update_data = user_schemas_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, request: Request):
    """Удалить пользователя"""
    user = await get_current_user(session=session, request=request)
    if not user:
        raise UserDontExist
    await session.delete(user)
    await session.commit()
    return {"detail": "success"}
