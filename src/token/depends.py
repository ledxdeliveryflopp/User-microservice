from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.depends import get_session, get_session_service
from src.settings.service import SessionService
from src.token.repository import TokenRepository
from src.token.service import TokenService


async def get_token_service(request: Request, session: AsyncSession = Depends(get_session),
                            session_service: SessionService = Depends(get_session_service)):
    token_repository = TokenRepository(session=session)
    token_service = TokenService(request=request, _token_repository=token_repository,
                                 _session_service=session_service)
    return token_service

