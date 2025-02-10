import json

from django.urls import reverse
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.test import APITestCase

from loja.fields import Conditions, Envios, Ofertas
from loja.models import Anuncio, Categoria, CustomUser


class AnuncioTestCase(APITestCase):
    def setUp(self):
        categoria = Categoria.objects.first()
        custom_user = CustomUser()

        custom_user.save()

        anuncio = Anuncio(
            categoria=categoria,
            usuario=custom_user,
            data_expirar=datetime.now(),
            ativo=True,
            views=0,
            titulo='Produto 1',
            descricao='Descrição do produto 1',
            preco=100.7,
            condicao=Conditions.NEW,
            envio=Envios.DHL,
            codigo_postal='40000-500',
            cidade='Salvador',
            rua='Rua A',
            numero=15,
            vendendo=True,
            tipo_oferta=Ofertas.FIXO,
            provedor='Fábrica 1',
            telefone='75999999999',
        )

        anuncio.save()

    def test_list_search(self):
        url = reverse('loja.anuncios-search')

        response = self.client.get(url, {'q': 'o', 'city': 'salvador'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 1)
