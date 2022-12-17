import json
import logging

import ccxt
from app import cache, scheduler
from flask import current_app as app

logger = logging.getLogger("app.schedule")


# @scheduler.task("interval", id="task-running", seconds=1)
# def every_second_task():
#     logger.info("running my task")

@scheduler.task("interval", id="task-get-binance", seconds=5)
def get_binance_tickers():
    data = ccxt.binance().fetch_tickers()
    NAME = str.upper("crypto_binance")
    cache.set(NAME, json.dumps(data))
    logger.info("get binance tickers")

@scheduler.task("interval", id="task-get-cryptocom", seconds=5)
def get_cryptocom_tickers():
    data = ccxt.cryptocom().fetch_tickers()
    NAME = str.upper("crypto_cryptocom")
    cache.set(NAME, json.dumps(data))
    logger.info("get crypto tickers")

# def setup_periodic_tasks(sender, **kwargs):
#     # sender.add_periodic_task(1.0, every_second_task, name='add-every-1')
#     sender.add_periodic_task(10.0, get_binance_tickers, name="get-binance-every-5")
#     sender.add_periodic_task(10.0, get_cryptocom_tickers, name="get-cryptocom-every-5")
