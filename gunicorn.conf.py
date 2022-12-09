import os
import multiprocessing

worker_class="eventlet"
bind = f"{os.getenv('HOST','0.0.0.0')}:{os.getenv('PORT',8080)}"
workers = multiprocessing.cpu_count()
pidfile = os.getenv("PIDFILE","run.pid")
accesslog = "-"
errorlog = "-"
access_log_format = '"%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
