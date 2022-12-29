import json
from django.shortcuts import render
from django.http.response import Http404
from django.core.cache import cache

# Create your views here.


def index(request):
    return render(request, 'index.html')


def get_pricing(request, exchange, symbol_a, symbol_b):
    c_exchange = str.upper(f"CRYPTO_{exchange}")
    symbol_A = str.upper(symbol_a)
    symbol_B = str.upper(symbol_b)
    r_data = cache.get(f"{c_exchange}")
    # if r_data is None:
    #     abort(404)
    result = json.loads(r_data)
    symbol_data = result.get(
        f"{symbol_A}/{symbol_B}", f"the symbol : {symbol_A}/{symbol_B} not exist."
    )
    # exist = True if type(symbol_data) is dict else False
    # system not symbol data
    # if not exist:
    #     abort(404)
    data = {"data": symbol_data, "exchange": exchange.upper()}
    # return render_template("price.html", data=data)

    print(r_data)
    return render(request, 'price.html', context=data)
