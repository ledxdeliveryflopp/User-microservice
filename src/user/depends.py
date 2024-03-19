from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.settings.depends import get_session, get_session_service
from src.settings.service import SessionService
from src.token.depends import get_token_service
from src.token.service import TokenService
from src.user.repository import UserRepository
from src.user.service import UserService


async def get_user_service(token_service: TokenService = Depends(
                           get_token_service), session: AsyncSession = Depends(get_session),
                           session_service: SessionService = Depends(get_session_service)):
    user_repository = UserRepository(_token_service=token_service, session=session)
    user_service = UserService(_session_service=session_service, _token_service=token_service,
                               _user_repository=user_repository)
    return user_service
