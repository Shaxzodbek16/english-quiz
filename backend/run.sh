#!/bin/bash

# shellcheck disable=SC2155
export PYTHONPATH=$(pwd)/app

alembic revision --autogenerate -m "Initial migration"

sleep 5

alembic upgrade head

python feed.py

black .

mypy .

uvicorn app.server.main:create_app --host 0.0.0.0 --port 8000 --reload --factory
