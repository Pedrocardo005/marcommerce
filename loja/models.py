from django.db import models
from django.utils.translation import gettext as _
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

    endereco = models.ForeignKey(
        'Endereco',
        models.CASCADE,
        blank=True,
        null=True,
        related_name='produtos'
    )

    def __str__(self):
        return '{} {}'.format(self.id, self.nome)
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        view = ProdutoView()
        view.produto = self
        view.save()
    

class ProdutoView(models.Model):

    views = models.IntegerField(default=0, blank=False, null=False)

    produto = models.OneToOneField(
        Produto,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='view',
        parent_link=False
    )


class Endereco(models.Model):

    bairro = models.CharField(max_length=255)

    cidade = models.CharField(max_length=255)

    estado = models.CharField(max_length=255)


class ImagemProduto(models.Model):

    nome = models.CharField(max_length=255)

    produto = models.ForeignKey(
        Produto,
        models.CASCADE,
        related_name='imagens'
    )

    imagem = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)

    def __str__(self) -> str:
        return '{} {}'.format(self.id, self.nome)
