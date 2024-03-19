from fastapi import FastAPI
from src.user.router import user_router

user = FastAPI()

user.include_router(user_router)


#test