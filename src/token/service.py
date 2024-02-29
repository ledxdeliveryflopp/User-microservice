from datetime import datetime
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.exceptions import TokenDontExist, TokenExpire
from src.settings.settings import Settings
from src.token.models import TokenModel
from jose import jwt


settings = Settings()


async def find_token(session: AsyncSession, token: str):
    """Поиск токена"""
    token = await session.execute(Select(TokenModel).filter(TokenModel.token == token))
    if not token:
        raise TokenDontExist
    return token.scalar()


async def verify_token(session: AsyncSession, request: Request):
    """Проверка токена"""
    header_token = request.headers.get('Authorization')
    header_token = header_token.replace("Bearer ", "")
    token = await find_token(session=session, token=header_token)
    if not token:
        raise TokenDontExist
    date = datetime.now()
    if token.expire < date:
        await session.delete(token)
        await session.commit()
        raise TokenExpire
    return token


async def get_token_payload(session: AsyncSession, request: Request):
    """Email пользователя из токена"""
    token = await verify_token(session=session, request=request)
    if not token:
        raise TokenDontExist
    token = token.token
    token_payload = jwt.decode(token=token, key=settings.secret_key, algorithms=settings.algorithm)
    user_email = token_payload.get("user_email")
    return user_email
