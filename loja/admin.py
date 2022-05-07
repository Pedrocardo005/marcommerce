from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Categoria, Produto
# Register your models here.

admin.site.register(Categoria, TranslatableAdmin)
admin.site.register(Produto, TranslatableAdmin)
