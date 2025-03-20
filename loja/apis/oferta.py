from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loja.models import Oferta, Venda
from loja.serializers import (AceitarOfertaSerializer, CreateOfertaSerializer,
                              OfertaAnuncioSerializer)


class CreateOferta(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            anuncio_id = request.data['id_anuncio']
            valor = request.data['valor']
            mensagem = request.data['mensagem']
            oferta = Oferta.objects.create(
                anuncio_id=anuncio_id, valor=valor,
                mensagem=mensagem
            )
            serializer = CreateOfertaSerializer(oferta)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'error': 'erro'}, status.HTTP_400_BAD_REQUEST)


class GetOfertas(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ofertas = Oferta.objects.filter(anuncio__usuario_id=request.user.pk)
        serializer = OfertaAnuncioSerializer(ofertas, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AceitarOferta(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            id_anuncio = request.data['id_anuncio']
            id_oferta = request.data['id_oferta']

            venda = Venda.objects.create(
                anuncio_id=id_anuncio,
                oferta_id=id_oferta
            )
            serializer = AceitarOfertaSerializer(venda)

            return Response(serializer.data, status.HTTP_201_CREATED)

        except Exception as error:
            return Response({'erro': str(error)}, status.HTTP_400_BAD_REQUEST)
