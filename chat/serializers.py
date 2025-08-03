from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import User, Chat, Message


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username:
            raise serializers.ValidationError('username is required')
        if not password:
            raise serializers.ValidationError('Password is required')
        return attrs



class UserSerializerWithName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserSerializerWithToken(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'is_superuser', 'access', 'refresh',
            'isAdmin',
        )

    def get_access(self, user: User):
        token: Token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user: User):
        token: Token = RefreshToken.for_user(user)
        return str(token)

    def get_isAdmin(self, user: User):
        return user.is_staff


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = [
            'id', 'name', 'is_active', 'is_group',
            'participants', 'sender', 'recipient', 'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'chat', 'file',
            'text', 'is_main', 'is_edited', 'is_deleted'
        ]