import json
from django.core.cache import cache
from core import celery_logger
from celery import shared_task

import ccxt


@shared_task(name="system-get-pricing")
def get_pricing():
    exchange_id = ['binance', 'cryptocom']
    for i in exchange_id:
        exchange_class = getattr(ccxt, i)
        exchange_data = exchange_class().fetch_tickers()
        NAME = str.upper(f"crypto_{i}")
        cache.set(NAME, json.dumps(exchange_data))
        celery_logger.info(f"GET {str.upper(i)} Exchange tickers data.")
