import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR.parent / ".env")
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://deepshield:deepshield@localhost:5432/deepshield")
JWT_SECRET = os.getenv("JWT_SECRET", "change-this-development-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 60
MAX_FILE_SIZE = 50 * 1024 * 1024
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")]
