from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from .models import CASUser as User
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware.csrf import get_token

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):
    """User serializer json field."""


    full_name = serializers.CharField(source='get_full_name')


    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'full_name']


class UserLoginSerializer(serializers.Serializer):
    """Serializer json field for login."""


    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            #email = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    'User with given username and password does not exists'
                )
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            username = user.username
            return {
                'username': user.username,
                'token': jwt_token
            }
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )


class AuthProfileDetailSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    is_waiter = serializers.SerializerMethodField()
    csrfmiddlewaretoken = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'


    def get_is_owner(self, obj):
        for market in obj.markets_owned_by.all():
            if market.url == settings.BASE_URL:
                return True
        return False
        

    def get_is_waiter(self, obj):
        for market in obj.waiters_owned_by.all():
            if market.url == settings.BASE_URL:
                return True
        return False

    def get_csrfmiddlewaretoken(self, obj):
        return get_token(self.context['request'])

    
