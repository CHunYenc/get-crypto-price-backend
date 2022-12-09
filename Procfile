web: gunicorn wsgi:app
worker: celery -A celery_worker.celery worker -P eventlet -c 1000 --loglevel=info
beat: celery -A celery_worker.celery beat -l info