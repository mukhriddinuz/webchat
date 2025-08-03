import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from pprint import pprint

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        pprint(self.scope)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        now = datetime.datetime.now().strftime("%H:%M:%S")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'time': now,
                'sender_channel': self.channel_name 
            }
        )

    async def chat_message(self, event):
        message = event['message']
        time = event['time']
        sender_channel = event['sender_channel'] 
        if self.channel_name == sender_channel:
            return

        await self.send(text_data=json.dumps({
            'message': message,
            'time': time
        }))



class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "online_users"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def receive(self, text_data):
