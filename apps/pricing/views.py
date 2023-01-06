import json
from django.shortcuts import render
from django.http.response import Http404
from django.core.cache import cache

# Create your views here.


def handler404(request, exception):
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


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
    c_exchange = str.upper(f"CRYPTO_{exchange}")
    symbol_A = str.upper(symbol_a)
    symbol_B = str.upper(symbol_b)
    r_data = cache.get(f"{c_exchange}")
    if r_data is None:
        raise Http404()
    result = json.loads(r_data)
    symbol_data = result.get(
        f"{symbol_A}/{symbol_B}", f"the symbol : {symbol_A}/{symbol_B} not exist."
    )
    exist = True if type(symbol_data) is dict else False
    # system not symbol data
    if not exist:
        raise Http404()
    return render(request, 'price.html', context={"data": symbol_data, "exchange": exchange.upper()})
