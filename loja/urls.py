from django.urls import path

from loja.views_loja.categoria import CategoriaListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('categories/', CategoriaListView.as_view(), name='categories'),
    path('languages/', views.languages, name='loja.languages'),
    path('product-details/<int:id>', views.product_details, name='loja.product-details'),
]
