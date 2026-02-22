from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from celery import Celery

# Database
db = SQLAlchemy()

# Redis Cache
cache = Cache()

# Celery instance
celery = Celery(__name__)
