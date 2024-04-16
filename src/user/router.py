from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.user.depends import get_user_service
from src.user.schemas import UserUpdateSchemas, UserBaseSchemas
from src.user.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

bearer_token = HTTPBearer()


@user_router.get("/all-user/", response_model=list[UserBaseSchemas])
async def get_all_users_router(limit: int = 100, offset: int = 0,
                               user: UserService = Depends(get_user_service)):
    return await user.get_all_users(limit=limit, offset=offset)


@user_router.get("/current-user/", response_model=UserBaseSchemas)
async def get_current_user_router(user: UserService = Depends(get_user_service)):
    """Роутер получения текущего пользователя"""
    return await user.get_current_user()


@user_router.patch("/update-user/", response_model=UserBaseSchemas)
async def update_user_router(schemas: UserUpdateSchemas, user: UserService = Depends(
                             get_user_service)):
    """Роутер обновления пользователя"""
    return await user.update_user(user_schemas_update=schemas)


@user_router.delete("/delete-user/")
async def delete_user_router(user: UserService = Depends(get_user_service)):
    """Роутер удаление пользователя"""
    return await user.delete_user()
