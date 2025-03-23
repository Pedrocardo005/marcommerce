from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loja.models import CustomUser
from loja.serializers import (ChangeUserFotoSerializer, EditUserSerializer,
                              RegisterUserSerializer)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format)


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = RegisterUserSerializer


class ChangeUserFotoView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        request.user.foto = request.data['foto']
        request.user.save()
        serializer = ChangeUserFotoSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class EditUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = EditUserSerializer(
            request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
