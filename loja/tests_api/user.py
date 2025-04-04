import json

from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

from loja.models import CustomUser
from loja.tests_api.baseRegistredUser import BaseRegistredUser

url_alterar_foto = reverse("loja.usuario-alterar-foto")
url_editar_usuario = reverse("loja.editar-usuario")
url_alterar_senha = reverse("loja.alterar-senha")
url_resetar_senha = reverse("loja.resetar-senha")
url_confirmar_resetar_senha = reverse("loja.confirmar-resetar-senha")


def mock_validate(self, attrs):
    return {"user": CustomUser.objects.first(), "new_password": "newpassword123"}


class UsuarioTestCase(BaseRegistredUser):
    def test_register_user(self):
        url = reverse("loja.register")

        data = {
            "email": "teste123@teste.com",
            "password": "12345678",
            "account_type": 1,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "email": "teste123@teste.com",
            "password": "12345678",
            "username": "teste123",
            "account_type": 1,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["email"], data["email"])
        self.assertEqual(response["username"], data["username"])
        self.assertEqual(response["account_type"], data["account_type"])
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_alterar_foto(self):
        self.login_loja()
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        image_data = BytesIO()
        image = Image.new("RGB", (100, 100), "white")
        image.save(image_data, format="png")
        image_data.seek(0)

        imagem = SimpleUploadedFile(
            "test1.png", image_data.read(), content_type="image/png"
        )

        data = {"foto": imagem}

        response = self.client.patch(
            url_alterar_foto,
            data,
            format="multipart",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertIsNotNone(response["foto"])

    def test_editar_usuario(self):

        data = {
            "email": "teste@gmail.com",
            "account_type": 1,
            "company_size": 1,
            "company_name": "texto qualquer",
            "first_name": "Primeiro nome",
            "last_name": "Ultimo nome",
            "street": "Rua a",
            "street_number": 14,
            "postcode": "40350-570",
            "city": "São Paulo",
            "commercial_provider": "Texto longo qualquer",
            "right_withdrawal": "Texto longo qualquer",
            "conditions": "Texto longo qualquer",
            "protection_notice": "Texto longo qualquer",
            "legal_notice": "Texto longo qualquer",
        }

        response = self.client.put(
            url_editar_usuario, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login_loja()

        response = self.client.put(
            url_editar_usuario, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["email"], "teste@gmail.com")
        self.assertEqual(response["company_name"], "texto qualquer")
        self.assertEqual(response["first_name"], "Primeiro nome")
        self.assertEqual(response["last_name"], "Ultimo nome")
        self.assertEqual(response["postcode"], "40350-570")
        self.assertEqual(response["city"], "São Paulo")
        self.assertEqual(response["commercial_provider"], "Texto longo qualquer")
        self.assertEqual(response["right_withdrawal"], "Texto longo qualquer")
        self.assertEqual(response["conditions"], "Texto longo qualquer")
        self.assertEqual(response["protection_notice"], "Texto longo qualquer")
        self.assertEqual(response["legal_notice"], "Texto longo qualquer")

        data = {**data, "legal_notice": "Texto modificado"}
        response = self.client.put(
            url_editar_usuario, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["legal_notice"], "Texto modificado")

        response = self.client.patch(
            url_editar_usuario, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_alterar_senha_usuario(self):
        self.login_loja()

        data = {
            "old_password": "secret",
            "new_password": "senha12345678",
            "repeat_password": "senha87654321",
        }
        response = self.client.patch(
            url_alterar_senha, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = {
            "new_password": "senha12345678",
            "repeat_password": "senha12345678",
        }
        response = self.client.patch(
            url_alterar_senha, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "old_password": "secret",
            "new_password": "senha12345678",
            "repeat_password": "senha12345678",
        }
        response = self.client.patch(
            url_alterar_senha, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("loja.serializers.PasswordResetConfirmSerializer.validate", mock_validate)
    def test_reset_senha_usuario(self):

        data = {"email": "teste1@teste.com"}
        response = self.client.post(url_resetar_senha, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"email": "teste@teste.com"}
        response = self.client.post(url_resetar_senha, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "uid": "uid-from-url",
            "token": "token-from-url",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        response = self.client.post(url_confirmar_resetar_senha, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["detail"], "Password has been reset successfully")

        self.login_loja("teste", "newpassword123")

        # Testa se login foi funcionou
        data = {
            "old_password": "newpassword123",
            "new_password": "senhaalterada",
            "repeat_password": "senhaalterada",
        }
        response = self.client.patch(
            url_alterar_senha, data, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
