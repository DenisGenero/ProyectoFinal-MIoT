import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

UY_TZ = ZoneInfo(os.getenv("TZ", "America/Montevideo"))

DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT", 3306)
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_NAME: str = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

CREATE_DB_CMD = f"CREATE DATABASE IF NOT EXISTS " +  (DB_NAME) + " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"

SECRET_KEY: str = os.getenv("SECRET_KEY")
SECRET_DISPOSITIVOS: str = os.getenv("SECRET_DISPOSITIVOS")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))