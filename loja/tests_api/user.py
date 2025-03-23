import json

from django.urls import reverse
from rest_framework import status

from loja.models import CustomUser
from loja.tests_api.baseRegistredUser import BaseRegistredUser

url_alterar_foto = reverse('loja.usuario-alterar-foto')


class UsuarioTestCase(BaseRegistredUser):
    def test_register_user(self):
        url = reverse('loja.register')

        data = {
            'email': 'teste123@teste.com',
            'password': '12345678',
            'account_type': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'email': 'teste123@teste.com',
            'password': '12345678',
            'username': 'teste123',
            'account_type': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['email'], data['email'])
        self.assertEqual(response['username'], data['username'])
        self.assertEqual(response['account_type'], data['account_type'])
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_alterar_foto(self):
        self.login_loja()
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(image_data, format='png')
        image_data.seek(0)

        imagem = SimpleUploadedFile(
            "test1.png", image_data.read(), content_type='image/png')

        data = {
            'foto': imagem
        }

        response = self.client.patch(url_alterar_foto, data, format='multipart', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertIsNotNone(response['foto'])
