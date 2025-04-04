from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loja.models import Anuncio, ChatRoom, Mensagem, Oferta, Venda
from loja.serializers import (AceitarOfertaSerializer, CreateOfertaSerializer,
                              OfertaAnuncioSerializer)


class CreateOferta(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            anuncio_id = request.data['id_anuncio']
            valor = request.data['valor']
            mensagem = request.data['mensagem']

            anuncio = Anuncio.objects.filter(id=anuncio_id).first()

            chat_room = ChatRoom.objects.create(
                nome=f'{request.user.id}_{anuncio.usuario.pk}'
            )

            obj_mensagem = Mensagem.objects.create(
                remetente=request.user,
                destinatario=anuncio.usuario,
                mensagem=mensagem,
                chat_room=chat_room
            )

            oferta = Oferta.objects.create(
                anuncio=anuncio, valor=valor,
                mensagem=obj_mensagem
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
