from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.user.depends import get_user_service
from src.user.schemas import UserBaseSchemas, UserUpdateSchemas
from src.user.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

bearer_token = HTTPBearer()


@user_router.get("/all-user/", response_model=list[UserBaseSchemas])
async def get_all_users_router(user: UserService = Depends(get_user_service),
                               token: str = Depends(bearer_token)):
    return await user.get_all_users()


@user_router.get("/current-user/", response_model=UserBaseSchemas)
async def get_current_user_router(user: UserService = Depends(get_user_service),
                                  token: str = Depends(bearer_token)):
    """Роутер получения текущего пользователя"""
    return await user.get_current_user()


@user_router.patch("/update-user/", response_model=UserBaseSchemas)
async def update_user_router(schemas: UserUpdateSchemas, user: UserService = Depends(
                             get_user_service), token: str = Depends(bearer_token)):
    """Роутер обновления пользователя"""
    return await user.update_user(user_schemas_update=schemas)


@user_router.delete("/delete-user/")
async def delete_user_router(user: UserService = Depends(get_user_service), token: str = Depends(
                             bearer_token)):
    """Роутер удаление пользователя"""
    return await user.delete_user()
