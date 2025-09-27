from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    

    # App
    app_name: str = "BookIt API"
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

