from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Categoria, Produto, Endereco, ImagemProduto, CustomUser, SubCategoria
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
admin.site.register(SubCategoria)
