import asyncio
import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class SymbolData:
    def __init__(self, exchange, symbol) -> None:
        self.exchange = exchange
        self.symbol = symbol


class RealTimePricingConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_message = None
        self.previous_data = None
        self.sent = False

    async def connect(self):
        await self.accept()
        await self.send_exchange_data()
        asyncio.ensure_future(self.update_data())

    async def disconnect(self, close_code):
        self.sent = False

    async def send_exchange_data(self):
        try:
            redis_data = cache.keys('CRYPTO_*')
            await self.send(text_data=json.dumps({"type": "exchange_list", "data": redis_data}))
        except Exception as e:
            logging.error(f"Failed to send exchange data: {str(e)}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json['type']
            message_data = text_data_json['data']
            print(text_data_json)
            if message_type == 'exchange_data':
                await self.send_symbol_list(message_data)
            elif message_type == "symbol_data":
                # 發送訊息
                await self.send_symbol_data(message_data)
        except Exception as e:
            logging.error(f"Failed to receive message: {str(e)}")

    async def send_symbol_list(self, message_data):
        try:
            redis_data = json.loads(cache.get(message_data))
            symbol_list = [i for i in redis_data]
            await self.send(text_data=json.dumps({"type": "symbol_list", "data": symbol_list}))
        except Exception as e:
            logging.error(f"Failed to send symbol list: {str(e)}")

    async def send_symbol_data(self, message_data):
        try:
            # init current_message
            current_message = SymbolData(
                exchange=message_data['exchange_data'], symbol=message_data['symbol_data'])
            # check current_message and self.previous_message
            if self.previous_message is None or self.previous_message.exchange != current_message.exchange or self.previous_message.symbol != current_message.symbol:
                logging.info(
                    'Exchange data or symbol data changed. Resubscribe is needed.')
                self.previous_message = current_message
            # get redis data
            current_data = json.loads(
                cache.get(self.previous_message.exchange, {}))
            if current_data is None or self.previous_message.symbol not in current_data:
                logging.warning(
                    f"No data for {self.previous_message.exchange} - {self.previous_message.symbol}")
                return

            current_data = current_data[self.previous_message.symbol]

            # send data
            logging.info(
                f'Pushed data. Exchange is {self.previous_message.exchange}, Symbol is {self.previous_message.symbol}')
            await self.send(text_data=json.dumps({"type": "symbol_data", "data": current_data}))
            self.sent = True
        except Exception as e:
            logging.error(f"Failed to send symbol data: {str(e)}")

    async def update_data(self):
        while True:
            await asyncio.sleep(5)
            if self.sent:
                logging.info(
                    f'Starting. Exchange is {self.previous_message.exchange}, Symbol is {self.previous_message.symbol}')
                current_data = json.loads(
                    cache.get(self.previous_message.exchange, {}))
                if current_data.get(self.previous_message.symbol) != self.previous_data:
                    self.previous_data = current_data.get(
                        self.previous_message.symbol)
                    await self.send(text_data=json.dumps({"type": "symbol_data", "data": self.previous_data}))
                else:
                    logging.info(
                        f'Exchange is {self.previous_message.exchange}, Symbol is {self.previous_message.symbol} Data is not change.')
