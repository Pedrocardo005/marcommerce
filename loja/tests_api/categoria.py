import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CategoriaTestCase(APITestCase):
    def test_get_all_cat_subcat(self):
        url = reverse('loja.cat-subcat')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 13)

        response = self.client.get(url, {'lang': 'en'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 0)

        response = self.client.get(url, {'lang': 'es'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 0)

    def test_get_all_categorias(self):
        url = reverse('loja.categorias')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 13)
