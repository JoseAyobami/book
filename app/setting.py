from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    environment: str = "development"
    database_url_local: str | None = None
    database_url_render: str | None = None
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    app_name: str = "BookIt API"
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        if self.environment == "production" and self.database_url_render:
            return self.database_url_render
        return self.database_url_local

settings = Settings()
