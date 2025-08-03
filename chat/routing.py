from django.urls import re_path
from .consumers import ChatConsumer, OnlineUsers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/user-status/$', OnlineUsers.as_asgi()),
]