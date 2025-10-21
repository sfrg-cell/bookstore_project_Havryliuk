from rest_framework import serializers
from django.contrib.auth.models import User
import logging

logger_i = logging.getLogger("i")
logger_w = logging.getLogger("w")


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    first_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    email = serializers.EmailField(max_length=50, required=True)
    password = serializers.CharField(style={'input_type': 'password'},
                write_only=True, min_length=8, max_length=50, required=True)
    password_check = serializers.CharField(style={'input_type': 'password'},
                write_only=True, min_length=8, max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_check']

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return data

    def create(self, data):
        try:
            user = User.objects.create_user(
                username=data['username'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data['email'],
                password=data['password'],
            )
            logger_i.info(f"Successfully registered a new user: {user.username}")
        except Exception as e:
            logger_w.warning(f"Failed to register a new user: {e}")
            raise e
        return user
