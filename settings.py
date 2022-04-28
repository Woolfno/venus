import dotenv
from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent
    ADMIN_TEMPLATES_DIR = BASE_DIR.joinpath('admin', 'templates')
    MEDIA_ROOT = BASE_DIR / 'media'
    REDIS_URL = ''
    DATABASE_URL = ''
    
    SECRET_KEY = ''
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    class Config:
        env_file = '.env'
    
settings = Settings()