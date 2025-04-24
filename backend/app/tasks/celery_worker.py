from celery import Celery
import time

from app.core.settings import get_settings, Settings

settings: Settings = get_settings()


app = Celery(
    "celery_worker",
    broker="pyamqp://guest:guest@rabbitmq:5672//",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.API_TRAFFIC_DB}",
)


@app.task
def test_task(msg: str = "Hello, world!") -> str:
    print("Test task executed")
    time.sleep(10)
    return f"{msg} - Task completed"


if __name__ == "__main__":
    app.start()
