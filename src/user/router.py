from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request
from src.user.depends import get_user_service
from src.user.schemas import UserBaseSchemas, UserUpdateSchemas
from src.user.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

bearer_token = HTTPBearer()


@user_router.get("/current-user/", response_model=UserBaseSchemas)
async def get_current_user_router(request: Request, user: UserService = Depends(
                                  get_user_service), token: str = Depends(bearer_token)):
    """Роутер получения текущего пользователя"""
    current_user = await user.get_current_user()
    return current_user


@user_router.patch("/update-user/", response_model=UserBaseSchemas)
async def update_user_router(schemas: UserUpdateSchemas, request: Request,
                             user: UserService = Depends(get_user_service),
                             token: str = Depends(bearer_token)):
    """Роутер обновления пользователя"""
    updated_user = await user.update_user(user_schemas_update=schemas)
    return updated_user


@user_router.delete("/delete-user/")
async def delete_user_router(request: Request, user: UserService = Depends(get_user_service),
                             token: str = Depends(bearer_token)):
    """Роутер удаление пользователя"""
    deleted_user = await user.delete_user()
    return user
