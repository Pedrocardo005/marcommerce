from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

class Categoria(TranslatableModel):
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        icone=models.CharField(max_length=255),
    )
    

class Produto(TranslatableModel):
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        preco=models.FloatField(blank=True, null=True, default=0),
        categoria=models.ForeignKey(
            Categoria,
            on_delete=models.CASCADE
        ),
    )
