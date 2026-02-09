from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "avito_bot",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    beat_schedule={
        "sync-avito-stats-daily": {
            "task": "app.tasks.avito_tasks.sync_all_stats",
            "schedule": 86400.0,  # every 24 hours
        },
        "send-scheduled-campaigns": {
            "task": "app.tasks.email_tasks.send_scheduled_campaigns",
            "schedule": 60.0,  # every minute
        },
    },
)
