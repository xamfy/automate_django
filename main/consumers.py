import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core import serializers

from .models import Device


class DeviceConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        # await asyncio.sleep(10)
        await self.send({
            "type": "websocket.send",
            "text": serializers.serialize('json', Device.objects.all(), fields=('name', 'status'))
        })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
