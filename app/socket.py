import json
import time

from flask_socketio import Namespace, emit
from flask import current_app as app
from app import cache


class MyCryptoPriceNamespace(Namespace):
    def on_connect(self):
        app.logger.info("connect.")
        k_prefix = cache.cache.key_prefix
        keys = cache.cache._write_client.keys(k_prefix + "*")
        keys = [k.decode("utf8") for k in keys]
        keys = [k.replace(k_prefix, "") for k in keys]
        emit("get_exchange", keys)
        self.status = False

    def on_disconnect(self):
        app.logger.info("disconnect.")
        self.status = False

    def on_get_symbol(self, data):
        key = f"{data['data']}"
        r_data = cache.get(key)
        symbol_list = json.loads(r_data)
        result = []
        for i in symbol_list:
            result.append(i)
        emit("get_symbol", result)

    def on_get_symbol_data(self, data):
        self.status = True
        self.exchange = data["exchange"].upper()
        self.symbol = data["symbol"].upper()
        while self.status:
            queryset = cache.get(f"{self.exchange}")
            result = json.loads(queryset)
            emit("get_symbol_data", result[self.symbol])
            time.sleep(10)
