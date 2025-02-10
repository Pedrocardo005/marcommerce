from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from loja.models import Anuncio
from loja.serializers import (GetAnuncioSerializer, SearchAnuncioSerializer,
                              UpdateAnuncioSerializer)


class SearchAnuncio(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('q', '')
        city_or_postal_code: str = request.query_params.get('city', '')

        # Verifica se é texto
        if city_or_postal_code.isalpha():
            anuncios = Anuncio.objects.filter(
                Q(cidade__icontains=city_or_postal_code) |
                Q(titulo__icontains=title)
            )
        else:
            anuncios = Anuncio.objects.filter(
                Q(codigo_postal__icontains=city_or_postal_code) |
                Q(titulo__icontains=title)
            )

        data = SearchAnuncioSerializer(anuncios, many=True).data
        return Response(data)


class GetAnuncio(generics.RetrieveUpdateDestroyAPIView):

    queryset = Anuncio

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateAnuncioSerializer
        return GetAnuncioSerializer
