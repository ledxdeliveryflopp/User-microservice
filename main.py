from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.user.router import user_router

user = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://localhost:6000",
    "http://localhost:5000",
]

user.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


user.include_router(user_router)

