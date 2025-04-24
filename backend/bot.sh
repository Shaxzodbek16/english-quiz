#!/bin/bash

alembic upgrade head

pip freeze > requirements.txt

export PYTHONPATH=$(pwd)

python app/bot/main.py
