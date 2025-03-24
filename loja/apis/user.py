from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from loja.models import CustomUser
from loja.serializers import (
    ChangeUserFotoSerializer,
    EditUserSerializer,
    RegisterUserSerializer,
)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format)


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = RegisterUserSerializer


class ChangeUserFotoView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        request.user.foto = request.data["foto"]
        request.user.save()
        serializer = ChangeUserFotoSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class EditUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = EditUserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="PATCH")


class ChangeUserPassword(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            repeat_password = request.data['repeat_password']

            if new_password != repeat_password:
                return Response({'msg': 'Senhas não conferem'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response({'msg': 'Senha alterada com sucesso'}, status.HTTP_200_OK)
            else:
                return Response({'msg': 'Senha incorreta'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        except Exception as error:
            return Response({'msg': f'Erro {str(error)}'}, status.HTTP_400_BAD_REQUEST)
