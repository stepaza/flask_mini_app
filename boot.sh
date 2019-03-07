#!/bin/sh

source /home/shopper/todo_venv/bin/activate

exec gunicorn -b :3200 --access-logfile - --error-logfile - wsgi:app