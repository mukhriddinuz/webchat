from asyncio import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from utils import render_data, render_message

from ...models import User, Chat, Message
from ...serializers import MessageSerializer


class MessageGenericAPIView(GenericAPIView):
    queryset = Message
    serializer_class = MessageSerializer


class ListMessageView(MessageGenericAPIView):

    def get(self, request):
        try:
            messages = self.queryset.objects.all().order_by('-created_at')
            serializer = self.serializer_class(messages, many=True)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK
            )

        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateMessageView(MessageGenericAPIView):

    def post(self, request):
        try:
            sender_id = request.data.get('sender')
            chat_id = request.data.get('chat')
            file = request.data.get('file')
            text = request.data.get('text')
            is_main = request.data.get('is_main', False)

            message = self.queryset.objects.create(
                sender_id=sender_id,
                chat_id=chat_id,
                file=file,
                text=text,
                is_main=is_main
            )

            serializer = self.serializer_class(message, many=False)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateMessageView(MessageGenericAPIView):

    def post(self, request, message_id):
        try:
            message = self.queryset.objects.get(id=message_id)
            serializer = self.serializer_class(
                instance=message, data=request.data, partial=True
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
        except Message.DoesNotExist:
            return Response(
                render_message(message='Message not found', success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteMessageView(MessageGenericAPIView):

    def post(self, request, message_id):
        try:
            message = self.queryset.objects.get(id=message_id)
            message.soft_delete()

            return Response(
                render_message(message='Message soft deleted', success='true'),
                status=status.HTTP_200_OK
            )
        except Message.DoesNotExist:
            return Response(
                render_message(message='Message not found', success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )