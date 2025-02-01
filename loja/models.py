from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _
from parler.models import TranslatableModel, TranslatedFields

from loja.fields import Conditions, Envios, Ofertas


class Categoria(TranslatableModel):

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        icone=models.CharField(max_length=255, blank=True, null=True),
    )

    def __str__(self):
        return self.nome


class Produto(TranslatableModel):
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        preco=models.FloatField(blank=True, null=True, default=0),
        descricao=models.TextField(blank=True, null=True, max_length=1000),
    )

    categoria = models.ForeignKey(
        Categoria, models.CASCADE, blank=True, null=True, related_name="produtos"
    )

    endereco = models.ForeignKey(
        "Endereco", models.CASCADE, blank=True, null=True, related_name="produtos"
    )

    created_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.id, self.nome)

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
        related_name="view",
        parent_link=False,
    )


class Endereco(models.Model):

    bairro = models.CharField(max_length=255)

    cidade = models.CharField(max_length=255)

    estado = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.estado, self.cidade, self.bairro)


class ImagemProduto(models.Model):

    nome = models.CharField(max_length=255)

    produto = models.ForeignKey(Produto, models.CASCADE, related_name="imagens")

    imagem = models.ImageField(
        _(""), upload_to=None, height_field=None, width_field=None, max_length=None
    )

    def __str__(self) -> str:
        return "{} {}".format(self.id, self.nome)


# Não se enquadra nos usuários do framework django.
class CustomUser(AbstractUser):

    # Adicione related_name aos campos groups e user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="customuser_groups",  # Adicione essa linha
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="customuser_user_permissions",  # Adicione essa linha
    )

    localizacao = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)

    foto = models.ImageField(
        _(""),
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )


class SubCategoria(models.Model):

    nome = models.TextField()

    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="subcategorias"
    )

    def __str__(self):
        return "{} - {}".format(self.categoria.nome, self.nome)


class MarcaArte(models.Model):

    nome = models.TextField()

    sub_categoria = models.ForeignKey(
        SubCategoria, on_delete=models.CASCADE, related_name="subcategorias"
    )

    def __str__(self):
        return "{} - {}".format(self.sub_categoria.nome, self.nome)


class Anuncio(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, related_name="anuncios"
    )

    usuario = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="anuncios"
    )

    data_expirar = models.DateTimeField()

    ativo = models.BooleanField()

    views = models.IntegerField()

    titulo = models.CharField(max_length=255)

    descricao = models.CharField(max_length=255)

    preco = models.DecimalField(decimal_places=2, max_digits=10)

    condicao = models.CharField(max_length=2, choices=Conditions.choices)

    envio = models.IntegerField(choices=Envios.choices)

    cidade = models.CharField(max_length=255)

    rua = models.CharField(max_length=255)

    numero = models.IntegerField()

    vendendo = models.BooleanField(default=True)

    tipo_oferta = models.IntegerField(choices=Ofertas.choices)

    provedor = models.CharField(max_length=255)

    telefone = models.CharField(max_length=255)

    data_venda = models.DateTimeField(auto_now_add=True)


class FotoAnuncio(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name="fotos")

    ordem = models.IntegerField()

    url_imagem = models.TextField()
