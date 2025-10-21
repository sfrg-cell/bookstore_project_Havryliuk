from user_auth.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
import logging

logger_i = logging.getLogger("i")
logger_w = logging.getLogger("w")


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        try:
            refresh = RefreshToken.for_user(user)
            logger_i.info(f"User {request.data['username']} logged in.")

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
        except Exception as e:
            logger_w.warning(f"Failed to login a new user: {e}")
            raise e


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            logger_i.info(f"User {request.data['username']} logged out.")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger_w.warning(f"Failed to logout: {e}")
            raise e
