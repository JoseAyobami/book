import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.setting import settings

if settings.environment == "production":
    DATABASE_URL = os.getenv("DATABASE_URL_RENDER")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_LOCAL")

if not DATABASE_URL:
    DATABASE_URL = settings.database_url  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

