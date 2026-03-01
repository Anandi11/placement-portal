from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from celery import Celery

db = SQLAlchemy()
cache = Cache()
celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]
)