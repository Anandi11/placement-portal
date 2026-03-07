from app import create_app
from extensions import celery
from celery.schedules import crontab

app=create_app()
app.app_context().push()

celery.conf.beat_schedule = {
    "daily-deadline-reminder": {
        "task": "tasks.send_deadline_reminders",
        "schedule": crontab(hour=9, minute=0), 
    },
    "monthly-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=10, minute=0),
    },
}