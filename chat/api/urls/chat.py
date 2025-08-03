from django.urls import path
from ..views.chat import ListChatView, CreateChatView, UpdateChatView, \
    DeleteChatView


urlpatterns = [
    path('list', ListChatView.as_view(), name='list'),
    path('create', CreateChatView.as_view(), name='create'),
    path('update/<int:chat_id>/', UpdateChatView.as_view(), name='update'),
    path('delete/<int:chat_id>/', DeleteChatView.as_view(), name='delete'),
]