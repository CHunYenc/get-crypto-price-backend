web: gunicorn core.asgi:application -w 2
worker: celery -A core.celery worker -l info -B