from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]['room_name']
        print("Connected to room:", self.room_name)

        await self.accept()  # <-- muhim!

    async def disconnect(self, close_code):
        print("Disconnected:", close_code)

    async def receive(self, text_data):
        print("Received:", text_data)
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type":"chat_message",
                "message":text_data_json['message'],
                "time":timezone.now().isoformat()
            }
        )

    async def chat_message(self, event):
        message = event['message']
        time = event['time']

        await self.send(text_data=json.dumps({
            'message': message,
            'time': time
        }))