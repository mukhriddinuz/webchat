from django.urls import path
from ..views.message import ListMessageView , CreateMessageView , UpdateMessageView , DeleteMessageView


urlpatterns = [
    path('list', ListMessageView.as_view(), name='list'),
    path('create', CreateMessageView.as_view(), name='create'),
    path('update/<int:message_id>/', UpdateMessageView.as_view(), name='update'),
    path('delete/<int:message_id>>/', DeleteMessageView.as_view(), name='delete'),
]