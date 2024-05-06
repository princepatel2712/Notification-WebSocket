import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected from django channels'}))

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'status': 'received'}))

    async def disconnect(self, code):
        print('disconnect')

    async def send_notification(self, event):
        event_data = json.loads(event['value'])
        user_id = self.scope['user'].id
        await self.send(text_data=json.dumps({'Count': event_data['count'],
                                              'Notification': event_data['current_notification'],
                                              'User': user_id}))
