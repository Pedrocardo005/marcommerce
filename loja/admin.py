from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from parler.admin import TranslatableAdmin

from .models import (Categoria, CustomUser, Endereco, ImagemProduto, Produto,
                     SubCategoria)

# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Outros campos',
            {
                'fields': (
                    'localizacao',
                    'foto',
                ),
            },
        ),
    )


admin.site.register(Categoria, TranslatableAdmin)
admin.site.register(Produto, TranslatableAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Endereco)
admin.site.register(ImagemProduto)
admin.site.register(SubCategoria, TranslatableAdmin)
