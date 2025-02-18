import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UsuarioTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('loja.register')

        data = {
            'email': 'teste@teste.com',
            'password': '12345678',
            'account_type': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'email': 'teste@teste.com',
            'password': '12345678',
            'username': 'teste',
            'account_type': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
