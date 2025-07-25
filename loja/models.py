from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _
from parler.models import TranslatableModel, TranslatedFields

from loja.fields import (AccountType, CompanySize, Conditions, Envios, Ofertas,
                         gerar_nome_aleatorio)
from loja.managers import CustomUserManager


class Categoria(TranslatableModel):

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
    )

    def __str__(self):
        return self.nome


class Produto(TranslatableModel):
    translations = TranslatedFields(
        nome=models.CharField(max_length=255),
        descricao=models.TextField(blank=True, null=True, max_length=1000),
    )

    categoria = models.ForeignKey(
        Categoria, models.CASCADE, blank=True, null=True, related_name="produtos"
    )

    endereco = models.ForeignKey(
        "Endereco", models.CASCADE, blank=True, null=True, related_name="produtos"
    )

    preco = models.FloatField(blank=True, null=True, default=0)

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

    produto = models.ForeignKey(
        Produto, models.CASCADE, related_name="imagens")

    imagem = models.ImageField(
        _(""), upload_to=gerar_nome_aleatorio, height_field=None, width_field=None, max_length=None
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

    localizacao = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, null=True)

    foto = models.ImageField(
        _(""),
        upload_to=gerar_nome_aleatorio,
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    # Campo já existente
    # data_criacao = models.DateTimeField(auto_now_add=True)

    account_type = models.IntegerField(
        choices=AccountType.choices, default=AccountType.IS
    )

    company_size = models.IntegerField(choices=CompanySize.choices, default=0)

    company_name = models.CharField(max_length=255, default="")

    street = models.CharField(max_length=255, default="")

    street_number = models.IntegerField(default=0)

    postcode = models.CharField(max_length=20, default="")

    city = models.CharField(max_length=255, default="")

    commercial_provider = models.TextField(default="")

    right_withdrawal = models.TextField(default="")

    conditions = models.TextField(default="")

    protection_notice = models.TextField(default="")

    legal_notice = models.TextField(default="")

    objects = CustomUserManager()


class SubCategoria(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=123),
    )

    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="subcategorias"
    )

    def __str__(self):
        return "{} - {}".format(self.categoria.nome, self.name)


class MarcaArte(models.Model):

    nome = models.TextField()

    sub_categoria = models.ForeignKey(
        SubCategoria, on_delete=models.CASCADE, related_name="subcategorias"
    )

    def __str__(self):
        return "{} - {}".format(self.sub_categoria.name, self.nome)


class Anuncio(models.Model):
    sub_categoria = models.ForeignKey(
        SubCategoria, on_delete=models.DO_NOTHING, related_name="anuncios", null=True
    )

    usuario = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="anuncios"
    )

    data_expirar = models.DateTimeField()

    ativo = models.BooleanField(default=True)

    views = models.IntegerField(blank=True, default=0)

    titulo = models.CharField(max_length=255)

    descricao = models.CharField(max_length=255)

    preco = models.DecimalField(decimal_places=2, max_digits=10)

    condicao = models.CharField(max_length=2, choices=Conditions.choices)

    envio = models.IntegerField(choices=Envios.choices)

    custo_envio = models.DecimalField(
        decimal_places=2, max_digits=10, default=0)

    pagamento_paypal = models.BooleanField(default=False)

    codigo_postal = models.CharField(max_length=10, default='')

    cidade = models.CharField(max_length=255)

    rua = models.CharField(max_length=255)

    numero = models.IntegerField(default=0)

    vendendo = models.BooleanField(default=True)

    tipo_oferta = models.IntegerField(choices=Ofertas.choices)

    provedor = models.CharField(max_length=255)

    telefone = models.CharField(max_length=255)

    data_publicacao = models.DateTimeField(auto_now_add=True)

    @property
    def url_foto(self):
        foto = self.fotos.first()
        if foto:
            return foto.imagem.url
        return ''


class FotoAnuncio(models.Model):
    anuncio = models.ForeignKey(
        Anuncio, on_delete=models.CASCADE, related_name="fotos")

    ordem = models.IntegerField()

    imagem = models.ImageField(upload_to=gerar_nome_aleatorio, null=True)

    class Meta:
        ordering = ['ordem']


class Oferta(models.Model):
    anuncio = models.ForeignKey(
        Anuncio, on_delete=models.CASCADE, related_name="ofertas"
    )

    valor = models.DecimalField(decimal_places=2, max_digits=10)

    mensagem = models.ForeignKey(
        'Mensagem', on_delete=models.DO_NOTHING, related_name='ofertas')

    data_hora = models.DateTimeField(auto_now_add=True, null=True)


class Venda(models.Model):
    anuncio = models.ForeignKey(
        Anuncio, on_delete=models.CASCADE, related_name="vendas"
    )

    oferta = models.ForeignKey(
        Oferta, on_delete=models.CASCADE, related_name="vendas")

    data_venda = models.DateTimeField(auto_now_add=True)


class Favorito(models.Model):
    usuario = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="favoritos"
    )

    anuncio = models.ForeignKey(
        Anuncio, on_delete=models.CASCADE, related_name="favoritos"
    )


class ChatRoom(models.Model):
    nome = models.CharField(max_length=100)


class Mensagem(models.Model):
    remetente = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="enviadas"
    )

    destinatario = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="recebidas"
    )

    mensagem = models.TextField()

    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='mensages', null=True)

    data_hora = models.DateTimeField(auto_now_add=True)


class SupportMessage(models.Model):
    assunto = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
