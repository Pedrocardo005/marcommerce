from django.urls import path
from knox import views as knox_views

from loja.apis.anuncio import (ChangeStatusAnuncio, CreateAnuncio,
                               DeteleFavoriteAnuncio, EditAnuncio,
                               FavoriteAnuncio, GetAllAnuncioCategoria,
                               GetAllAnuncioSubCategoria, GetAnuncio,
                               GetAnunciosUsuario, SearchAnuncio)
from loja.apis.categoria import AllCategorias, CatSubCat
from loja.apis.oferta import AceitarOferta, CreateOferta, GetOfertas
from loja.apis.user import (ChangeUserFotoView, EditUserView, LoginView,
                            RegisterUserView, ChangeUserPassword)

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
    path("register/", RegisterUserView.as_view(), name='loja.register'),
    path("anuncios/usuario/<int:pk>", GetAnunciosUsuario.as_view(),
         name='loja.anuncios-usuario'),
    path('anuncios/', CreateAnuncio.as_view(), name='loja.anuncios-criar'),
    path('anuncios/change_status/<int:pk>',
         ChangeStatusAnuncio.as_view(), name='loja.anuncio-change-status'),
    path('anuncios/favorite/', FavoriteAnuncio.as_view(),
         name='loja.favorite-anuncio'),
    path('anuncios/favorite/<int:pk>', DeteleFavoriteAnuncio.as_view(),
         name='loja.delete-favorite-anuncio'),
    path('anuncios/ofertar', CreateOferta.as_view(), name='loja.ofertar-anuncio'),
    path('anuncios/ofertados', GetOfertas.as_view(),
         name='loja.ofertados-anuncios'),
    path('ofertas/aceitar', AceitarOferta.as_view(), name='loja.aceitar-ofertas'),
    path('usuarios/alterar-foto', ChangeUserFotoView.as_view(),
         name='loja.usuario-alterar-foto'),
    path('usuarios/editar_usuario', EditUserView.as_view(),
         name='loja.editar-usuario'),
     path('usuarios/alterar_senha', ChangeUserPassword.as_view(), name='loja.alterar-senha')
]
