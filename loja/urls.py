from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('languages/', views.languages, name='loja.languages'),
    path('product-details/', views.product_details, name='loja.product-details'),
]
