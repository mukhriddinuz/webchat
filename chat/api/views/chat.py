from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from utils import render_data, render_message

from ...models import User, Chat
from ...serializers import ChatSerializer
