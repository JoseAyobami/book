from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str

    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    admin_name: str
    admin_email: str
    admin_password: str

    # App
    app_name: str = "BookIt API"
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

# import os
# print(os.environ.get("refresh_token_expire_days"))
# print(os.environ.get("refresh_acess_token"))  # Should be None or removed
