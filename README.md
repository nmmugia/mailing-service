# Mailing Service
This repository contains service that solves mail scheduling problem.


## Set Up environment and init the database


```bash
python manage.py init_database
```

## Run the celery (worker to do the scheduled task)

```bash
celery -A scheduler.main.celery worker --detach --pidfile=''
```

## tests
```bash
pytest -vv
```

## how to run the service 
```bash
python manage.py run -h 0.0.0.0
```
it will be served in localhost:5000
