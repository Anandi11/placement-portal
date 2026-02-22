import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "super-secret-key"

    # 🔥 FIXED SQLite path (inside backend folder)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = "redis://localhost:6379/0"

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL

    JWT_SECRET_KEY = "jwt-secret-key"

