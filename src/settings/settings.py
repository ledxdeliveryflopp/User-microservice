from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "1ca26a466e6327dfd6e51599fd2892e59ba1a2885ab3d9b09f48baaa3ca2251c"
    algorithm: str = "HS256"
    sql_url: str = "postgresql+asyncpg://postgres:postgres@database:5432/postgres"
