from logging.config import dictConfig
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_caching import Cache
from pathlib import Path
from celery import Celery
from app.settings import config

import os
import redis
import logging

import eventlet

eventlet.monkey_patch()
socketio = SocketIO()
celery = Celery(__name__)
cache = Cache(config={"CACHE_TYPE": "RedisCache"})


INIT_LOGGING = "Init |"


def page_not_found(e):
    return render_template("404.html"), 404


def internal_server_error(e):
    return render_template("500.html"), 500


def make_celery(app):
    celery.conf.result_backend = f"{app.config['CELERY_RESULT_BACKEND']}/2"
    celery.conf.broker_url = f"{app.config['CELERY_BROKER_URL']}/1"
    # TODO Use SSL
    # if 'rediss://' in app.config['REDIS_URL']:
    #     celery.conf.broker_use_ssl = {
    #         'ssl_cert_reqs': ssl.CERT_REQUIRED
    #     }
    #     celery.conf.redis_backend_use_ssl = {
    #         'ssl_cert_reqs': ssl.CERT_REQUIRED
    #     }
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return app


def check_logs_folder(LOGS_FOLDER):
    """ckeck app/logs folder"""
    logging.info(f"{INIT_LOGGING} LOGS FOLDER EXIST ? {os.path.isdir(LOGS_FOLDER)}")
    if not os.path.isdir(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)
        logging.info(f"{INIT_LOGGING} CREATE {LOGS_FOLDER} FOLDER !!!")
    else:
        logging.info(f"{INIT_LOGGING} EXISTED LOGS FOLDER.")


def create_app(env):
    BASE_DIR = Path(__file__).resolve().parent
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    check_logs_folder(LOGS_DIR)
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "flask": {
                    "level": "INFO",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": os.path.join(LOGS_DIR, "app.log"),
                    "formatter": "default",
                },
                "celery": {
                    "level": "INFO",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": os.path.join(LOGS_DIR, "celery.log"),
                    "formatter": "default",
                },
            },
            "loggers": {
                "": {"level": "INFO", "handlers": ["flask", "default"]},
                "app.celery": {"handlers": ["celery", "default"], "level": "INFO"},
            },
        }
    )
    app = Flask(__name__)
    app.config.from_object(config[env])
    app.logger.info(f"{INIT_LOGGING} LOADING ENV = {env}")

    with app.app_context():
        # celery
        make_celery(app)
        from app import tasks

        # Caching
        cache.init_app(app)
        # blueprint
        from app.views import simple_page

        # error page handler
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(500, internal_server_error)
        app.register_blueprint(simple_page)
        # socket_io
        from app.socket import MyCryptoPriceNamespace

        socketio.on_namespace(MyCryptoPriceNamespace("/"))
        socketio.init_app(
            app,
            cors_allowed_origins="*",
            message_queue=f"{app.config['REDIS_URL']}/3",
            async_mode="eventlet",
            engineio_logger=True,
        )
    return app
