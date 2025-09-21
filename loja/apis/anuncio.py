from django.db.models import Q
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loja.models import Anuncio, Favorito
from loja.pagination import SmallResultsSetPagination
from loja.serializers import (AnuncioUsuarioSerializer,
                              ChangeStatusAnuncioSerializer,
                              CreateAnuncioSerializer,
                              CreateFavoriteAnuncioSerializer,
                              FirstThreeAnuncioSerializer,
                              GetAnuncioSerializer, SearchAnuncioSerializer,
                              UpdateAnuncioSerializer)


class SearchAnuncio(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        title = request.query_params.get("q", "")
        city_or_postal_code: str = request.query_params.get("city", "")
        category_id: str = request.query_params.get("category", "")

        # Verifica se é texto
        if city_or_postal_code.isalpha():
            anuncios = Anuncio.objects.filter(
                Q(cidade__icontains=city_or_postal_code) | Q(
                    titulo__icontains=title)
            )
        else:
            anuncios = Anuncio.objects.filter(
                Q(codigo_postal__icontains=city_or_postal_code)
                | Q(titulo__icontains=title)
            )

        if category_id:
            anuncios = anuncios.filter(
                sub_categoria__categoria__id=int(category_id))

        data = SearchAnuncioSerializer(anuncios, many=True).data
        return Response(data)


class GetAnuncio(generics.RetrieveUpdateDestroyAPIView):

    queryset = Anuncio

    def update(self, request, *args, **kwargs):
        anuncio = Anuncio.objects.filter(pk=kwargs["pk"]).first()
        if request.user.id == anuncio.usuario.pk or self.request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        raise NotAuthenticated

    def delete(self, request, *args, **kwargs):
        anuncio = Anuncio.objects.filter(pk=kwargs["pk"]).first()
        if request.user.id == anuncio.usuario.pk or self.request.user.is_superuser:
            return super().delete(request, *args, **kwargs)
        raise NotAuthenticated

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateAnuncioSerializer
        return GetAnuncioSerializer


class EditAnuncio(generics.RetrieveAPIView):
    queryset = Anuncio
    serializer_class = UpdateAnuncioSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        anuncio = Anuncio.objects.filter(pk=kwargs["pk"]).first()
        if request.user.id == anuncio.usuario.pk or self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise NotAuthenticated


class GetAllAnuncioSubCategoria(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        sub_categoria_id = kwargs["pk"]
        anuncios = Anuncio.objects.filter(sub_categoria__id=sub_categoria_id)
        data = SearchAnuncioSerializer(anuncios, many=True).data
        return Response(data, status.HTTP_200_OK)


class GetAllAnuncioCategoria(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        categoria_id = kwargs["pk"]
        anuncios = Anuncio.objects.filter(
            sub_categoria__categoria__id=categoria_id).order_by('pk')
        data = SearchAnuncioSerializer(anuncios, many=True).data
        return Response(data, status.HTTP_200_OK)


class GetAnunciosUsuario(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultsSetPagination
    serializer_class = AnuncioUsuarioSerializer

    def get_queryset(self):
        user = self.request.user
        return user.anuncios.order_by('pk')


class CreateAnuncio(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        anuncio = request.data.copy()
        anuncio['usuario_id'] = request.user.id
        fotos = []
        for key, value in request.data.items():
            if key.startswith('fotos[') and key.endswith('].imagem'):
                # Extrai o índice da foto
                index = key.split('[')[1].split(']')[0]
                ordem = anuncio.pop(f'fotos[{index}].ordem')

                anuncio.pop(f'fotos[{index}].imagem')

                # Adiciona a foto à lista
                fotos.append({
                    'imagem': value,
                    'ordem': ordem
                })

        if len(fotos):
            anuncio['fotos'] = fotos
        serializer = CreateAnuncioSerializer(data=anuncio)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ChangeStatusAnuncio(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        anuncio_id = kwargs["pk"]
        anuncio = Anuncio.objects.filter(pk=anuncio_id).first()
        if request.user.id == anuncio.usuario.pk or request.user.is_superuser:
            vendendo = request.data['vendendo']
            anuncio.vendendo = vendendo
            anuncio.save()
            data = ChangeStatusAnuncioSerializer(anuncio).data
            return Response(data, status.HTTP_200_OK)
        raise NotAuthenticated


class FavoriteAnuncio(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            id_user = request.user.pk
            id_anuncio = request.data['id_anuncio']
            favorito = Favorito.objects.create(
                usuario_id=id_user, anuncio_id=id_anuncio)
            serializer = CreateFavoriteAnuncioSerializer(favorito)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except:
            return Response({'error': 'erro'}, status.HTTP_400_BAD_REQUEST)


class DeteleFavoriteAnuncio(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFavoriteAnuncioSerializer
    queryset = Favorito


class GetThreeFirstAnuncio(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        anuncios = Anuncio.objects.order_by('-id')[:3]
        anuncios = sorted(anuncios, key=lambda x: x.id)
        data = FirstThreeAnuncioSerializer(anuncios, many=True).data
        return Response(data)
