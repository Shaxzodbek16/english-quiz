from celery import Celery
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

app = Celery(
    "celery_worker",
    broker="pyamqp://guest:guest@rabbitmq:5672//",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.API_TRAFFIC_DB}",
)

app.autodiscover_tasks(
    [
        "app.core.tasks",
    ]
)

