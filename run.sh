#!/bin/bash

pip freeze > requirements.txt

black .

mypy .

rm -rf app/core/migrations/versions/*

alembic revision --autogenerate -m "init"

alembic upgrade head

python feed.py

uvicorn app.server.main:create_app --host 0.0.0.0 --port 8000 --reload --factory
