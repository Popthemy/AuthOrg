from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserSerializer, RegisterUserSerializer, LoginUserSerializer
from .models import User

# Create your views here.


def get_jwt_token(user):
    try:
        token = RefreshToken.for_user(user=user)
        return token
    except Exception as e:
        return Response({
            "status": "Error",
            "message": "Error generating refresh token",
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterUserView(APIView):
    serializer_class = RegisterUserSerializer

    def get(self, request):
        serializer = UserSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh_token = get_jwt_token(user)

            response_data = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh_token.access_token),
                    "user": serializer.data
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh_token = get_jwt_token(user)

            response_data = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh_token.access_token),
                    "user": UserSerializer(date=user)
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": status.HTTP_401_UNAUTHORIZED
        }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer)
