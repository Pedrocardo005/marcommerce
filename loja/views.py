from django.shortcuts import render

from loja.models import Categoria

# Create your views here.

def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def categories(request):
    categorias = Categoria.objects.all()
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


def languages(request):
    return render(request, 'languages.html')
