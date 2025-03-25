import json

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from loja.fields import Conditions, Envios, Ofertas
from loja.models import Anuncio, CustomUser, SubCategoria


class BaseRegistredUser(APITestCase):
    token = None

    def setUp(self):
        subcategoria = SubCategoria.objects.first()
        custom_user = CustomUser()
        custom_user.email = "teste@teste.com"
        custom_user.username = "teste"
        custom_user.set_password("secret")

        custom_user.save()

        anuncio = Anuncio(
            sub_categoria=subcategoria,
            usuario=custom_user,
            data_expirar=timezone.now(),
            ativo=True,
            views=0,
            titulo="Produto 1",
            descricao="Descrição do produto 1",
            preco=100.7,
            condicao=Conditions.NEW,
            envio=Envios.DHL,
            codigo_postal="40000-500",
            cidade="Salvador",
            rua="Rua A",
            numero=15,
            vendendo=True,
            tipo_oferta=Ofertas.FIXO,
            provedor="Fábrica 1",
            telefone="75999999999",
        )

        anuncio.save()

    def login_loja(self, username="teste", password="secret"):

        url_login = reverse("knox_login")
        data_login = {"username": username, "password": password}

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode("utf-8"))
        self.token = response_login["token"]

    def logout_loja(self):
        url_logout = reverse("knox_logout")
        self.client.post(url_logout, headers={"Authorization": f"Bearer {self.token}"})
