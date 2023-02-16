import asyncio
import json
import logging

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.cache import cache


class RealTimePricingConsumer(AsyncWebsocketConsumer):
    sent = False

    async def connect(self):
        await self.accept()
        await self.send_exchange_data()

    async def disconnect(self, close_code):
        pass

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
            if message_type == 'exchange_data':
                await self.send_symbol_list(message_data)
            elif message_type == "symbol_data":
                self.sent = True
                while self.sent:
                    await self.send_symbol_data(message_data)
                    await asyncio.sleep(10)
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
            redis_data = json.loads(cache.get(message_data['exchange_data']))[message_data['symbol_data']]
            await self.send(text_data=json.dumps({"type": "symbol_data", "data": redis_data}))
        except Exception as e:
            logging.error(f"Failed to send symbol data: {str(e)}")
