#!/bin/bash

alembic upgrade head

python feed.py

pip freeze > requirements.txt

export PYTHONPATH=$(pwd)

python app/bot/main.py
