from django.urls import path
from .views import index, get_messages, room

urlpatterns = [
    path('', index),
    path('get_messages', get_messages),
    path("chat/<str:room_name>/", room, name="room"),

]