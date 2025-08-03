# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils import timezone
from .models import Message, User, Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get token from headers
        try:
            headers = dict(self.scope['headers'])
            auth_header = headers.get(b'authorization', b'').decode('utf-8')
            
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                user = await self.get_user_from_token(token)
                print(user)
                if user and not isinstance(user, AnonymousUser):
                    self.user = user
                    print(f"User authenticated: {self.user.status}")
                    self.room_name = self.scope['url_route']['kwargs']['chat_id']
                    self.room_group_name = f'chat_{self.room_name}'
                    
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    await self.accept()
                    await self.fetch_history(self.room_name)
                    return
        except Exception as e:
            print(f"Connection error: {str(e)}")
        
        # Close connection if authentication fails
        await self.close()

    @database_sync_to_async
    def get_user_from_token(self, token):
        """Helper method to get user from JWT token"""
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        except (InvalidToken, TokenError) as e:
            print(f"Token validation failed: {str(e)}")
            return AnonymousUser()
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return AnonymousUser()

    async def disconnect(self, close_code):
        """Clean up on disconnect"""
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming messages"""
        try:
            data = json.loads(text_data)
            message = data['message']
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                    'senderid': self.user.id,
                    'chat_id': self.room_name,
                    'created_at': str(timezone.now())
                }
            )
        except Exception as e:
            print(f"Message handling error: {str(e)}")

    async def chat_message(self, event):
        """Send message to WebSocket"""
        time = await self.get_time_save(event)
        if self.scope["user"].id != event["senderid"]:
            await self.send(text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
                "created_at": event["created_at"]
            }))

    @database_sync_to_async
    def get_time_save(self, data):
        message = Message.objects.create(
            sender_id=data['senderid'],
            chat_id=data['chat_id'],
            text=data['message'],
        )
        print(data)
        return message.created_at
    
    async def fetch_history(self, chat_id):
        messages = await self.history_messages(chat_id)
        for message in messages:
            await self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def history_messages(self, chat_id):
        messages = Message.objects.filter(chat_id=chat_id).order_by('-created_at')
        return [
            {
                'sender': message.sender.username,
                'message': message.text,
                'created_at': message.created_at.isoformat()
            } for message in messages
        ]
        

class OnlineUsers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'online_users'
        try:
            headers = dict(self.scope['headers'])
            auth_header = headers.get(b'authorization', b'').decode('utf-8')
            print(f"Connecting to online users with header: {auth_header}")
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                user = await self.get_user_from_token(token)
                print(user)
                if user and not isinstance(user, AnonymousUser):
                    status = await self.user_status(user.id, 'Online')
                    print(status)
        except Exception as e:
            print(f"Error connecting to online users: {str(e)}")
            await self.close()
            return
        await self.accept()

    async def disconnect(self, close_code):
        print(self.scope['user'])
        status = await self.user_status(self.scope['user'].id, timezone.now())
        await self.close()

    async def user_status(self, user_id, status):
        message_status = await self.edit_user_status(user_id, status)
        return message_status
    
    @database_sync_to_async
    def edit_user_status(self, user_id, status):
        user = User.objects.get(id=user_id)
        print(f"User status updated: {user.username} is now {status}")
        user.is_online = status
        user.save()
        return True
    
