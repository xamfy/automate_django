import asyncio
import json
from django.contrib.auth.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core import serializers

from channels.generic.websocket import AsyncWebsocketConsumer


from .models import Device


class DeviceConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        me = self.scope['user']
        objects = await self.get_devices(me)
        # print(me)
        # print(objects)
        # await asyncio.sleep(10)
        # await self.send({
        #     "type": "websocket.send",
        #     "text": serializers.serialize('json', Device.objects.all(), fields=('name', 'status'))
        # })
        user_room = f"room_{me}"
        print(f"room:{user_room}")
        self.user_room = user_room

        await self.channel_layer.group_add(
            user_room,
            self.channel_name
        )

        # await self.send({
        #     "type": "websocket.accept"
        # })
        await self.accept()

    async def websocket_receive(self, event):
        print("receive", event)
        # print(event['text'])
        # objects = await self.set_device_status(event['text'], self.scope['user'])
        # print(objects)
        data = event.get('text', None)
        if data is not None:
            dict_data = json.loads(data)
            name = dict_data['name']
            status = dict_data['status']
            print(f"{name} : {status}")
            response = {
                'name': name,
                'status': status
            }
            # new_event = {
            #     "type": "device_status",
            #     "text": json.dumps(response)
            # }
            # await self.send({
            #     "type": "websocket.send",
            #     "text": json.dumps(response)
            # })
        # new_event = {
        #     "type": "websocket.send",
        #     "text": "hi"
        # }
            await self.channel_layer.group_send(
                self.user_room,
                {
                    "type": "device_status",
                    "text": response
                }
            )

    async def device_status(self, event):
        # message = event['text']

        print('message', event['text'])
        await self.send(text_data=json.dumps(event['text']))
        # await self.send(text_data=json.dumps({
        #     'text': message
        # }))

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_devices(self, user):
        return User.objects.filter(username=user).values_list('devices', flat=True)

    @database_sync_to_async
    def set_device_status(self, status, user):
        return Device.objects.filter(owner=user)
