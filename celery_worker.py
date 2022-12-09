from app import create_app

app = create_app("production")
# app = create_app("development")
app.app_context().push()

from app import celery

# Use eventlet
# celery -A celery_worker.celery worker -P eventlet -c 1000 --loglevel=info
# celery -A celery_worker.celery beat -l info