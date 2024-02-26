from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.settings.depends import get_session
from src.user.schemas import UserBaseSchemas
from src.user.service import get_current_user

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

bearer_token = HTTPBearer()


@user_router.get("/current-user/", response_model=UserBaseSchemas)
async def get_current_user_router(request: Request, token: str = Depends(bearer_token), session:
                                  AsyncSession = Depends(get_session)):
    """Роутер получения текущего пользователя"""
    user = await get_current_user(session=session, request=request)
    return user

