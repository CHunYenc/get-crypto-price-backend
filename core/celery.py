import logging
import os
from kombu import Exchange, Queue

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

default_exchange = Exchange('default', type="direct")
scheduler_exchange = Exchange('scheduler', type="direct")
# system_exchange = Exchange('system', type="direct")

queue = (
    Queue('default', exchange=default_exchange, routing_key='default'),
    Queue('schedule_task', exchange=scheduler_exchange,
          routing_key='schedule_task'),
    # Queue('system_task', exchange=system_exchange, routing_key='system_task'),
)

# 定義工作列隊
route = {
    # 主要執行 settings.py 程式
    # 'system*': {'queue': "system_task", "routing_key": "system_task"},
    '*': {'queue': 'default', 'routing_key': 'default'}
}

app.conf.update(task_queues=queue, task_routes=route)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

logger = logging.getLogger('django.celery')

# development
# celery -A core.celery worker -l info -B
# online
# celery -A core.celery worker --loglevel=info
# celery -A core.celery beat -l info
