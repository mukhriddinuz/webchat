from asyncio import exceptions
from urllib import request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from utils import render_data, render_message

from ...models import User, Chat
from ...serializers import ChatSerializer


class ChatGenericAPIView(GenericAPIView):
    queryset = Chat
    serializer_class = ChatSerializer


class ListChatView(ChatGenericAPIView):

    def get(self, request):
        try:
            chats = self.queryset.objects.all().order_by('-id')
            serializer = self.serializer_class(chats, many=True)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK
            )

        except Exception as error:
            return Response(
                render_message(message=error, success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateChatView(ChatGenericAPIView):

    def post(self, request):
        try:
            name = request.data.get('name')
            is_active = request.data.get('is_active')
            created_at = request.data.get('created_at')
            date = request.data.get('date')
            is_group = request.data.get('is_group')
            participants = request.data.get('participants')
            sender = request.data.get('sender')
            recipient = request.data.get('recipient')

            group = self.queryset.objects.create(
                name=name,
                is_active=is_active,
                created_at=created_at,
                date=date,
                is_group=is_group,
                participants=participants,
                sender=sender,
                recipient=recipient
            )

            serializer = self.serializer_class(group, many=False)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=error, success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateChatView(ChatGenericAPIView):

    def post(self, chat_id):
        try:
            chat = self.queryset.objects.get(id=chat_id)
            serializer = self.serializer_class(
                instance=chat, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    render_data(data=serializer.data, success='true'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    render_message(message=serializer.errors, success='false'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message='Chat not found', success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteChatView(ChatGenericAPIView):

    def post(self, chat_id):
        try:
            chat = self.queryset.objects.get(id=chat_id)
            chat.delete()

            return Response(
                render_message(message='Chat deleted', success='true'),
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response(
                render_message(message='Chat not found', success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )