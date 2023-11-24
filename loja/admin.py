from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Categoria, Produto, Endereco, ImagemProduto
# Register your models here.

admin.site.register(Categoria, TranslatableAdmin)
admin.site.register(Produto, TranslatableAdmin)
admin.site.register(Endereco)
admin.site.register(ImagemProduto)
