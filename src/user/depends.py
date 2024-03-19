from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.depends import get_session_repository
from src.settings.repository import SessionRepository
from src.token.depends import get_token_repository
from src.token.repository import TokenRepository
from src.user.repository import UserRepository
from src.user.service import UserService


async def get_user_service(request: Request, session_repository:
                           SessionRepository = Depends(get_session_repository),
                           token_repository: TokenRepository = Depends(get_token_repository)):
    user_repository = UserRepository(request=request, session_repository=session_repository,
                                     token_repository=token_repository)
    user_service = UserService(repository=user_repository)
    return user_service
