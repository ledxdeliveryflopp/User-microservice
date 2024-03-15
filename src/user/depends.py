from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.depends import get_session
from src.user.repository import UserRepository
from src.user.service import UserService


async def get_user_service(request: Request, session: AsyncSession = Depends(get_session)):
    user_repository = UserRepository(request=request, session=session)
    user_service = UserService(repository=user_repository)
    return user_service
