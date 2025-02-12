import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from loja.fields import Conditions, Envios, Ofertas
from loja.models import Anuncio, CustomUser, SubCategoria


class AnuncioTestCase(APITestCase):
    def setUp(self):
        subcategoria = SubCategoria.objects.first()
        custom_user = CustomUser()
        custom_user.username = 'teste'
        custom_user.set_password('secret')

        custom_user.save()

        anuncio = Anuncio(
            sub_categoria=subcategoria,
            usuario=custom_user,
            data_expirar=timezone.now(),
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
        anuncio = response[0]
        self.assertEqual(anuncio['titulo'], 'Produto 1')
        self.assertEqual(anuncio['descricao'], 'Descrição do produto 1')
        self.assertEqual(anuncio['preco'], 100.7)
        self.assertEqual(anuncio['condicao'], Conditions.NEW)

    def test_get_anuncio(self):
        url = reverse('loja.get-anuncio', kwargs={'pk': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['titulo'], 'Produto 1')
        self.assertEqual(response['preco'], 100.7)
        self.assertEqual(response['views'], 0)
        self.assertEqual(response['id_anunciante'], 1)
        self.assertEqual(response['email_anunciante'], '')

    def test_update_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse('loja.get-anuncio', kwargs={'pk': anuncio.pk})
        self.client.login(username='teste', password='secret')

        data = {
            "vendendo": True,
            "titulo": "Fiat Palio",
            "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
            "tipo_oferta": 1,
            "preco": 40000.00,
            "condicao": Conditions.SECOND_HAND,
            "envio": 2,
            "pagamento_paypal": True,
            "codigo_postal": "40000-000",
            "cidade": "São Paulo",
            "rua": "Rua São Marcelo",
            "numero": 12,
            "provedor": "Casas Bahia",
            "telefone": "71984287792"
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['vendendo'], True)
        self.assertEqual(response['titulo'], 'Fiat Palio')
        self.assertEqual(response['codigo_postal'], '40000-000')
        self.assertEqual(response['rua'], 'Rua São Marcelo')

        custom_user = CustomUser()
        custom_user.username = 'teste 2'
        custom_user.set_password('secret2')

        custom_user.save()

        self.client.logout()
        self.client.login(username='teste 2', password='secret2')

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 403)

    def test_remove_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse('loja.get-anuncio', kwargs={'pk': anuncio.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        custom_user = CustomUser()
        custom_user.username = 'teste 2'
        custom_user.set_password('secret2')

        custom_user.save()

        self.client.login(username='teste 2', password='secret2')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        self.client.logout()

        self.client.login(username='teste', password='secret')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
