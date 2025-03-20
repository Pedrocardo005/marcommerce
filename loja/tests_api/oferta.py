import json

from django.urls import reverse
from rest_framework import status

from loja.models import Anuncio, Oferta
from loja.tests_api.baseRegistredUser import BaseRegistredUser

url_ofertar_anuncio = reverse('loja.ofertar-anuncio')
url_anuncios_ofertados = reverse('loja.ofertados-anuncios')
url_aceitar_oferta = reverse('loja.aceitar-ofertas')


class OfertaTestCase(BaseRegistredUser):
    def test_ofertar_anuncio(self):
        self.login_loja()

        anuncio = Anuncio.objects.last()

        data = {
            'valor': 1500.00,
            'mensagem': 'Mensagem indicando interesse no produto'
        }
        response = self.client.post(url_ofertar_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'id_anuncio': anuncio.pk,
            'valor': 1500.00,
            'mensagem': 'Mensagem indicando interesse no produto'
        }
        response = self.client.post(url_ofertar_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['mensagem'], data['mensagem'])
        self.assertEqual(Oferta.objects.count(), 1)

        self.logout_loja()

        response = self.client.post(url_ofertar_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_traz_anuncios_ofertados(self):
        self.login_loja()

        anuncio = Anuncio.objects.last()

        data = {
            'id_anuncio': anuncio.pk,
            'valor': 1500.00,
            'mensagem': 'Mensagem indicando interesse no produto'
        }
        for _ in range(3):
            response = self.client.post(url_ofertar_anuncio, data, headers={
                'Authorization': f'Bearer {self.token}'
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url_anuncios_ofertados, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 3)

    def test_aceitar_oferta(self):
        self.login_loja()

        anuncio = Anuncio.objects.last()

        data = {
            'id_anuncio': anuncio.pk,
            'valor': 1500.00,
            'mensagem': 'Mensagem indicando interesse no produto'
        }
        response = self.client.post(url_ofertar_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['mensagem'], data['mensagem'])
        id_oferta = response['id']

        data = {
            "id_anuncio": anuncio.pk,
            "id_oferta": id_oferta
        }
        response = self.client.post(url_aceitar_oferta, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
