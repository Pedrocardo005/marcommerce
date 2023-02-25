from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Categoria(TranslatableModel):

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        icone=models.CharField(max_length=255, blank=True, null=True),
    )

    categoria=models.ForeignKey(
        'Categoria',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='categorias'
    )

    def __str__(self):
        return self.nome
    

class Produto(TranslatableModel):
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        preco=models.FloatField(blank=True, null=True, default=0),
        categoria=models.ForeignKey(
            Categoria,
            on_delete=models.CASCADE
        ),
    )

    def __str__(self):
        return '{} {}'.format(self.id, self.nome)
