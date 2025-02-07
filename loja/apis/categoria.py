from rest_framework import generics
from rest_framework.response import Response

from loja.models import Categoria
from loja.serializers import CategoriaSerializer


class CatSubCat(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'pt')
        categorias = Categoria.objects.translated(lang)
        data = CategoriaSerializer(categorias, many=True).data
        return Response(data)


class AllCategorias(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'pt')
        categorias = Categoria.objects.translated(lang)
        data = CategoriaSerializer(categorias, many=True, context={
                                   'show_subcategorias': False}).data
        return Response(data)
