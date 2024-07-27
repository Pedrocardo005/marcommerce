from django.shortcuts import render

# Create your views here.

def index(request):
    try:
        return render(request, 'index.html')
    except:
        return render(request, '404.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def languages(request):
    return render(request, 'languages.html')


def product_details(request, id):
    return render(request, 'product-details.html')
