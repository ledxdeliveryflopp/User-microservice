from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.depends import get_session
from src.token.repository import TokenRepository
from src.token.service import TokenService


async def get_token_service(request: Request, session: AsyncSession = Depends(get_session)):
    token_repository = TokenRepository(request=request, session=session)
    token_service = TokenService(repository=token_repository)
    return token_service
