from django.urls import path

from loja.apis.categoria import CatSubCat

urlpatterns = [
    path('cat-subcat/', CatSubCat.as_view(), name='loja.cat-subcat')
]
