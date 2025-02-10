from django.urls import path

from loja.apis.anuncio import SearchAnuncio
from loja.apis.categoria import AllCategorias, CatSubCat

urlpatterns = [
    path('cat-subcat/', CatSubCat.as_view(), name='loja.cat-subcat'),
    path('categorias/', AllCategorias.as_view(), name='loja.categorias'),
    path('listsearch/', SearchAnuncio.as_view(), name='loja.anuncios-search')
]
