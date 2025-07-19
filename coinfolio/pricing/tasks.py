import json
from django.core.cache import cache
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

import ccxt


@shared_task(name="system-get-pricing")
def get_pricing():
    """
    透過 ccxt 取得交易所的 tickers 資料，並存入 cache 中。
    
    manual run:
    python manage.py shell
    from coinfolio.pricing.tasks import get_pricing
    get_pricing()
    get_pricing.delay()
    
    celery beat run:
    celery -A config.celery_app worker -l info
    celery -A config.celery_app beat -l info --scheduler=config.celery.beat_schedule
    """
    exchange_id = ['binance']
    for i in exchange_id:
        exchange_class = getattr(ccxt, i)
        try:
            exchange_data = exchange_class().fetch_tickers()
            logger.info(f"Successfully fetched tickers for {str.lower(i)}.")
            NAME = str.lower(f"{i}")
            logger.info(f"Successfully fetched {len(exchange_data)} tickers for {NAME}")
            
            # 方法2: 直接使用 Redis
            try:
                import redis
                from django.conf import settings
                redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
                r = redis.from_url(redis_url)
                
                # 使用 Django cache 的 key 格式
                cache_key = f":1:coinfolio:{NAME}"  # Django cache key format
                r.set(cache_key, json.dumps(exchange_data))
                logger.info(f"Method 2: SET {NAME} to Redis directly SUCCESS")
            except Exception as redis_e:
                logger.error(f"Method 2: Direct Redis FAILED: {redis_e}")
        except ccxt.NetworkError as e:
            logger.error(f"Network error while fetching tickers for {i}: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error while fetching tickers for {i}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching tickers for {i}: {e}")
