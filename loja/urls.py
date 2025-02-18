from django.urls import path
from knox import views as knox_views

from loja.apis.anuncio import (EditAnuncio, GetAllAnuncioCategoria,
                               GetAllAnuncioSubCategoria, GetAnuncio,
                               SearchAnuncio)
from loja.apis.categoria import AllCategorias, CatSubCat
from loja.apis.user import LoginView, RegisterUserView

urlpatterns = [
    path("cat-subcat/", CatSubCat.as_view(), name="loja.cat-subcat"),
    path("categorias/", AllCategorias.as_view(), name="loja.categorias"),
    path("listsearch/", SearchAnuncio.as_view(), name="loja.anuncios-search"),
    path("anuncios/<int:pk>", GetAnuncio.as_view(), name="loja.get-anuncio"),
    path("anuncios/edit/<int:pk>", EditAnuncio.as_view(), name="loja.edit-anuncio"),
    path(
        "anuncios/subcategoria/<int:pk>",
        GetAllAnuncioSubCategoria.as_view(),
        name="loja.anuncios-subcategoria",
    ),
    path("anuncios/categoria/<int:pk>", GetAllAnuncioCategoria.as_view(),
         name='loja.anuncios-categoria'),
    path("login/", LoginView.as_view(), name='knox_login'),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("register/", RegisterUserView.as_view(), name='loja.register')
]
