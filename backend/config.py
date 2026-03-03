import datetime

class Config:
    SECRET_KEY = "secret"
    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=3)
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    
    # Email Config (Gmail example)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "anandiraghavi2005@gmail.com"
    MAIL_PASSWORD = "brvhhmnsxwpovdly"
    MAIL_DEFAULT_SENDER = "anandiraghavi2005@gmail.com"