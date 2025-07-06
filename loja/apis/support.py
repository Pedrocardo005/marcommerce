from rest_framework import generics

from loja.serializers import SupportMessageSerializer


class SendSupportMessage(generics.CreateAPIView):
    serializer_class = SupportMessageSerializer
