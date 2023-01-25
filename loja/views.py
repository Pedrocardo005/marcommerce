import traceback
from django.shortcuts import render

from loja.models import Categoria, CategoriaTranslation

# Create your views here.

def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def categories(request):
    try:
        categorias = Categoria.objects.filter(categoria__isnull=True)
        lista_categorias = []

        for categoria in categorias:
            c = {
                'nome': categoria.nome,
                'icone': categoria.icone
            }

            lista_categorias.append(c)

        context = {
            'categorias': lista_categorias
        }

        return render(request, 'categories.html', context)
    except Exception as error:
        print('O erro:', error)
        print(traceback.format_exc())
        return render(request, 'categories.html')


def languages(request):
    return render(request, 'languages.html')
