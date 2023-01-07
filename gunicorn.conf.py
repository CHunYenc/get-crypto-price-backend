# gunicorn core.asgi:application

import os
import multiprocessing

bind = f"{os.getenv('HOST','0.0.0.0')}:{os.getenv('PORT','8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() // 2
pidfile = os.getenv("PIDFILE", "gunicorn.pid")
accesslog = "-"
errorlog = "-"
access_log_format = '"%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
