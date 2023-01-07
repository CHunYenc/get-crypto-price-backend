web: gunicorn wsgi:app
worker: celery -A core.celery worker -l info -B