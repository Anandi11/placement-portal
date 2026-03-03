from app import create_app
from extensions import celery

app = create_app()
app.app_context().push()

from celery.schedules import crontab

celery.conf.beat_schedule = {
    "daily-deadline-reminder": {
        "task": "tasks.send_deadline_reminders",
        "schedule": crontab(hour=9, minute=0),  # Runs every day at 9 AM
    },
    "monthly-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=10, minute=0),  # 1st of month
    },
}