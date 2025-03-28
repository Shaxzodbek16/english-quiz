#!/bin/bash

pip freeze > requirements.txt

export PYTHONPATH=$(pwd)

black .

mypy .

python app/bot/main.py
