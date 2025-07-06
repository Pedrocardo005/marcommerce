import json

from django.urls import reverse
from rest_framework.test import APITestCase

url_send_suport_message = reverse('loja.send-support-message')


class SupportTestCase(APITestCase):
    def test_send_support_message(self):

        data = {
            'assunto': 'Pergunta geral',
            'mensagem': 'Teste 123, testando mensagem.'
        }

        response = self.client.post(url_send_suport_message, 400)

        data = {
            'assunto': 'Pergunta geral',
            'email': 'example@example.com',
        }

        response = self.client.post(url_send_suport_message, 400)

        data = {
            'assunto': 'Pergunta geral',
            'email': 'example@example.com',
            'mensagem': 'Teste 123, testando mensagem.'
        }

        response = self.client.post(url_send_suport_message, data)
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['assunto'], data['assunto'])
        self.assertEqual(response['email'], data['email'])
        self.assertEqual(response['mensagem'], data['mensagem'])
