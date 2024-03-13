from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):

    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SqlSettings(BaseSettings):
    sql_user: str
    sql_password: str
    sql_host: str
    sql_port: str
    sql_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class UrlSettings(BaseSettings):
    user_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):

    jwt_settings: JwtSettings
    sql_settings: SqlSettings
    url_settings: UrlSettings


settings = Settings(jwt_settings=JwtSettings(), sql_settings=SqlSettings(),
                    url_settings=UrlSettings())
