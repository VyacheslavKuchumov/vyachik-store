from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    ADMIN_EMAIL: str = "admin@mail.ru"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    # to get a secure secret key, run:
    # openssl rand -hex 32
    SECRET_KEY: str = "UNSECURE_SECRET_KEY_CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()