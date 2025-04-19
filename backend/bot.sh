#!/bin/bash

alembic upgrade head

python feed.py

pip freeze > requirements.txt

export PYTHONPATH=$(pwd)

black .

mypy .

python app/bot/main.py
