import os
import multiprocessing
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# gunicorn variables
worker_class = "eventlet"
bind = f"{os.getenv('HOST','0.0.0.0')}:{os.getenv('PORT',8080)}"
workers = 1
pidfile = os.getenv("PIDFILE", "run.pid")
accesslog = "-"
errorlog = "-"
access_log_format = '"%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
