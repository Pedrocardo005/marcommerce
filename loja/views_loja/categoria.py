from django.views.generic import ListView

from loja.models import Categoria


class CategoriaListView(ListView):
    model = Categoria
    