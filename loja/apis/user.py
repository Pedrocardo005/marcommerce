from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from loja.models import CustomUser
from loja.serializers import ChangeUserFotoSerializer, RegisterUserSerializer


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
    def patch(self, request, *args, **kwargs):
        request.user.foto = request.data['foto']
        request.user.save()
        serializer = ChangeUserFotoSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)
