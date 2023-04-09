#!/bin/sh
python manage.py init_database
celery -A scheduler.main.celery worker --loglevel=INFO --detach --pidfile=''
python manage.py run -h 0.0.0.0