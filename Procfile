web: gunicorn core.asgi:application
worker: celery -A core.celery worker -l info -B