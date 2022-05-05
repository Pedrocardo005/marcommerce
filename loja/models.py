from django.db import models

# Create your models here.

class Categoria(models.Model):
    
    nome = models.CharField(max_length=255)
    icone = models.CharField(max_length=255)


class Produto(models.Model):

    nome = models.CharField(max_length=255)
    preco = models.FloatField(blank=True, null=True, default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )