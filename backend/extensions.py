from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from celery import Celery
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]
)
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "daily-deadline-reminder": {
        "task": "tasks.send_deadline_reminders",
        "schedule": crontab(hour=9, minute=0),
    },
    "monthly-admin-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=8, minute=0),
    },
}