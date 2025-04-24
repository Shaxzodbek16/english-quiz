FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh bot.sh

EXPOSE 8000

CMD ["sh", "-c", "./run.sh & ./bot.sh & celery -A app.tasks.celery_worker worker --loglevel=info & wait"]