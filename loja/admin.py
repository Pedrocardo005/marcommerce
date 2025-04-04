from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from parler.admin import TranslatableAdmin

from .models import (Anuncio, Categoria, ChatRoom, CustomUser, Endereco,
                     FotoAnuncio, ImagemProduto, Mensagem, Produto,
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
admin.site.register(Anuncio)
admin.site.register(FotoAnuncio)
admin.site.register(ChatRoom)
admin.site.register(Mensagem)
