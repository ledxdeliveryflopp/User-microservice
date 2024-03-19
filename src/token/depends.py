from fastapi import Depends
from starlette.requests import Request
from src.settings.depends import get_session_repository
from src.settings.repository import SessionRepository
from src.token.repository import TokenRepository


async def get_token_repository(request: Request, session_repository:
                               SessionRepository = Depends(get_session_repository)):
    token_repository = TokenRepository(request=request, session_repository=session_repository)
    return token_repository
