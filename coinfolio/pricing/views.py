from django import template
import json
import logging
from django.shortcuts import render
from django.http.response import Http404
from django.core.cache import cache 
from django.http import HttpResponse

# Create your views here.
from django.conf import settings

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'pricing/index.html', {'DEBUG': settings.DEBUG})


def get_pricing(request, exchange, symbol_a, symbol_b):
    """讓 Google Sheet 透過 XML 的方式同步價格。

    Args:
        request (_type_): _description_
        exchange (_type_): _description_
        symbol_a (_type_): _description_
        symbol_b (_type_): _description_

    Returns:
        _type_: _description_
    """
    c_exchange = str.lower(f"{exchange}")
    symbol_A = str.upper(symbol_a)
    symbol_B = str.upper(symbol_b)
    
    # 直接使用 Redis
    import redis
    from django.conf import settings
    
    redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
    cache_key = f":1:coinfolio:{c_exchange}"
    
    # 只在 Redis 連線和資料操作時使用 try
    try:
        r = redis.from_url(redis_url)
    except Exception as conn_e:
        logger.error(f"Redis connection FAILED: {conn_e}")
        return HttpResponse(f"Redis connection error: {conn_e}")
    
    try:
        data = r.get(cache_key)
        if data:
            logger.info(f"GET {c_exchange} from Redis SUCCESS")
        else:
            logger.warning(f"No data found for key: {cache_key}")
    except Exception as data_e:
        logger.error(f"Redis data retrieval FAILED: {data_e}")
    # 取得 data 下的交易對
    result = json.loads(data)
    symbol_data = result.get(
        f"{symbol_A}/{symbol_B}", f"the symbol : {symbol_A}/{symbol_B} not exist."
    )
    exist = True if type(symbol_data) is dict else False
    # system not symbol data
    if not exist:
        logging.info(
            f"The {c_exchange}'s {symbol_A}/{symbol_B} data not exist.")
        raise Http404()
    # 如果沒有漲跌幅度時，提供一個漲跌幅度
    if symbol_data['percentage'] is None:
        symbol_data['percentage'] = float(symbol_data['info']['c']) * 100
    return render(request, 'pricing/price.html', context={"data": symbol_data, "exchange": exchange.upper()})
        
        

def get_websocket_pricing(request):
    return render(request, 'pricing/price_ws.html')
