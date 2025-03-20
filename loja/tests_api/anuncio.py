import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from loja.fields import Conditions, Envios, Ofertas
from loja.models import Anuncio, CustomUser, Oferta, SubCategoria
from loja.tests_api.baseRegistredUser import BaseRegistredUser

url_favorite_anuncio = reverse('loja.favorite-anuncio')
url_ofertar_anuncio = reverse('loja.ofertar-anuncio')
url_anuncios_ofertados = reverse('loja.ofertados-anuncios')
url_aceitar_oferta = reverse('loja.aceitar-ofertas')


class AnuncioTestCase(BaseRegistredUser):

    def test_list_search(self):
        url = reverse("loja.anuncios-search")

        response = self.client.get(url, {"q": "o", "city": "salvador"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response), 1)
        anuncio = response[0]
        self.assertEqual(anuncio["titulo"], "Produto 1")
        self.assertEqual(anuncio["descricao"], "Descrição do produto 1")
        self.assertEqual(anuncio["preco"], 100.7)
        self.assertEqual(anuncio["condicao"], Conditions.NEW)

    def test_get_anuncio(self):
        anuncio = Anuncio.objects.filter(
            titulo="Produto 1", descricao="Descrição do produto 1"
        ).first()
        url = reverse("loja.get-anuncio", kwargs={"pk": anuncio.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["titulo"], "Produto 1")
        self.assertEqual(response["preco"], 100.7)
        self.assertEqual(response["views"], 0)
        self.assertEqual(response["id_anunciante"], anuncio.usuario.pk)
        self.assertEqual(response["email_anunciante"], "")

    def test_update_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse("loja.get-anuncio", kwargs={"pk": anuncio.pk})

        # Faz login no sistema
        self.login_loja()

        sub_categoria = SubCategoria.objects.last()

        data = {
            "vendendo": True,
            "sub_categoria_id": sub_categoria.pk,
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
            "telefone": "71984287792",
        }

        response = self.client.put(url, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["vendendo"], True)
        self.assertEqual(response["titulo"], "Fiat Palio")
        self.assertEqual(response["codigo_postal"], "40000-000")
        self.assertEqual(response["rua"], "Rua São Marcelo")
        self.assertEqual(response["sub_categoria_id"], sub_categoria.pk)

        custom_user = CustomUser()
        custom_user.username = "teste 2"
        custom_user.set_password("secret2")

        custom_user.save()

        # Logout
        self.logout_loja()

        # Faz login no sistema
        self.login_loja('teste 2', 'secret2')

        response = self.client.put(url, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse("loja.get-anuncio", kwargs={"pk": anuncio.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        custom_user = CustomUser()
        custom_user.username = "teste 2"
        custom_user.set_password("secret2")

        custom_user.save()

        self.login_loja('teste 2', 'secret2')

        response = self.client.delete(url, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.logout_loja()
        self.login_loja()

        response = self.client.delete(url, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse("loja.edit-anuncio", kwargs={"pk": anuncio.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login_loja()

        response = self.client.get(url, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response["titulo"], anuncio.titulo)
        self.assertEqual(response["preco"], float(anuncio.preco))
        self.assertEqual(response["custo_envio"], str(anuncio.custo_envio))
        self.assertEqual(response["codigo_postal"], anuncio.codigo_postal)
        self.assertEqual(response["cidade"], anuncio.cidade)
        self.assertEqual(response["rua"], anuncio.rua)
        self.assertEqual(response["numero"], anuncio.numero)
        self.assertEqual(response["provedor"], anuncio.provedor)
        self.assertEqual(response["telefone"], anuncio.telefone)

    def test_get_anuncios_by_sub_categoria(self):
        subcategoria = SubCategoria.objects.last()
        custom_user = CustomUser.objects.first()

        anuncios = []
        for idx in range(0, 5):
            anuncio = Anuncio(
                sub_categoria=subcategoria,
                usuario=custom_user,
                data_expirar=timezone.now(),
                ativo=True,
                views=0,
                titulo=f"Produto {idx + 2}",
                descricao=f"Descrição do produto {idx + 2}",
                preco=100.7,
                condicao=Conditions.NEW,
                envio=Envios.DHL,
                codigo_postal="40000-500",
                cidade="Salvador",
                rua="Rua A",
                numero=15,
                vendendo=True,
                tipo_oferta=Ofertas.FIXO,
                provedor=f"Fábrica {idx + 2}",
                telefone="75999999999",
            )

            anuncio.save()
            anuncios.append(anuncio)
        url = reverse("loja.anuncios-subcategoria",
                      kwargs={"pk": subcategoria.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response), 5)

        for idx, anuncio in enumerate(anuncios):
            self.assertEqual(response[idx]['id'], anuncio.id)
            self.assertEqual(response[idx]['titulo'], anuncio.titulo)
            self.assertEqual(response[idx]['descricao'], anuncio.descricao)
            self.assertEqual(response[idx]['preco'], anuncio.preco)
            self.assertEqual(response[idx]['condicao'], anuncio.condicao)

    def test_get_anuncios_by_categoria(self):
        subcategoria = SubCategoria.objects.last()
        custom_user = CustomUser.objects.first()

        anuncios = []
        for idx in range(0, 5):
            anuncio = Anuncio(
                sub_categoria=subcategoria,
                usuario=custom_user,
                data_expirar=timezone.now(),
                ativo=True,
                views=0,
                titulo=f"Produto {idx + 2}",
                descricao=f"Descrição do produto {idx + 2}",
                preco=100.7,
                condicao=Conditions.NEW,
                envio=Envios.DHL,
                codigo_postal="40000-500",
                cidade="Salvador",
                rua="Rua A",
                numero=15,
                vendendo=True,
                tipo_oferta=Ofertas.FIXO,
                provedor=f"Fábrica {idx + 2}",
                telefone="75999999999",
            )

            anuncio.save()
            anuncios.append(anuncio)

        url = reverse('loja.anuncios-categoria',
                      kwargs={'pk': subcategoria.categoria.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 5)

        for idx, anuncio in enumerate(anuncios):
            self.assertEqual(response[idx]['id'], anuncio.id)
            self.assertEqual(response[idx]['titulo'], anuncio.titulo)
            self.assertEqual(response[idx]['descricao'], anuncio.descricao)
            self.assertEqual(response[idx]['preco'], anuncio.preco)
            self.assertEqual(response[idx]['condicao'], anuncio.condicao)

    def test_get_anuncio_by_usuario(self):
        subcategoria = SubCategoria.objects.last()
        custom_user = CustomUser()
        custom_user.username = "teste2"
        custom_user.set_password("secret2")

        custom_user.save()
        url = reverse('loja.anuncios-usuario', kwargs={
            'pk': custom_user.pk
        })

        anuncios = []
        for idx in range(0, 5):
            anuncio = Anuncio(
                sub_categoria=subcategoria,
                usuario=custom_user,
                data_expirar=timezone.now(),
                ativo=True,
                views=idx,
                titulo=f"Produto {idx + 2}",
                descricao=f"Descrição do produto {idx + 2}",
                preco=100.7 + idx,
                condicao=Conditions.NEW,
                envio=Envios.DHL,
                codigo_postal="40000-500",
                cidade="Salvador",
                rua="Rua A",
                numero=15,
                vendendo=True,
                tipo_oferta=Ofertas.FIXO,
                provedor=f"Fábrica {idx + 2}",
                telefone="75999999999",
            )

            anuncio.save()
            anuncios.append(anuncio)

        self.login_loja('teste2', 'secret2')

        response = self.client.get(url, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 5)

        for idx, anuncio in enumerate(anuncios):
            self.assertEqual(response[idx]['id'], anuncio.id)
            self.assertEqual(response[idx]['ativo'], anuncio.ativo)
            self.assertEqual(response[idx]['views'], anuncio.views)
            self.assertEqual(response[idx]['preco'], anuncio.preco)

    def test_create_anuncio(self):
        self.login_loja()

        url = reverse('loja.anuncios-criar')

        sub_categoria = SubCategoria.objects.last()

        data = {
            "sub_categoria_id": sub_categoria.pk,
            "data_expirar": "24/10/2100",
            "ativo": True,
            "vendendo": True,
            "titulo": "Fiat Palio 2015",
            "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
            "preco": 40000.00,
            "tipo_oferta": 1,
            "condicao": "SH",
            "envio": 2,
            "pagamento_paypal": True,
            "codigo_postal": "40000-000",
            "cidade": "São Paulo",
            "rua": "Rua São Marcelo",
            "numero": 12,
            "provedor": "Casas Bahia",
            "telefone": "71984287792"
        }

        response = self.client.post(url, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['ativo'], True)
        self.assertEqual(response['vendendo'], True)
        self.assertEqual(response['titulo'], "Fiat Palio 2015")
        self.assertEqual(
            response['descricao'], "Carro seminovo em perfeito estado, 10.000km rodados")
        self.assertEqual(response['cidade'], "São Paulo")

        data.pop('sub_categoria_id')

        response = self.client.post(url, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content.decode('utf-8'))

        # Test criar anuncio com imagens

        data['sub_categoria_id'] = sub_categoria.pk
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(image_data, format='png')
        image_data.seek(0)

        imagem1 = SimpleUploadedFile(
            "test1.png", image_data.read(), content_type='image/png')
        image_data.seek(0)  # Reinicia o ponteiro do arquivo
        imagem2 = SimpleUploadedFile(
            "test2.png", image_data.read(), content_type='image/png')

        data['fotos[0].imagem'] = imagem1
        data['fotos[0].ordem'] = 1
        data['fotos[1].imagem'] = imagem2
        data['fotos[1].ordem'] = 2

        response = self.client.post(url, data, format='multipart', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        fotos = response.get('fotos')
        self.assertIsNotNone(fotos)

    def test_change_status(self):
        self.login_loja()

        url_create_anuncio = reverse('loja.anuncios-criar')

        sub_categoria = SubCategoria.objects.last()

        data = {
            "sub_categoria_id": sub_categoria.pk,
            "data_expirar": "24/10/2100",
            "ativo": True,
            "vendendo": True,
            "titulo": "Fiat Palio 2015",
            "descricao": "Carro seminovo em perfeito estado, 10.000km rodados",
            "preco": 40000.00,
            "tipo_oferta": 1,
            "condicao": "SH",
            "envio": 2,
            "pagamento_paypal": True,
            "codigo_postal": "40000-000",
            "cidade": "São Paulo",
            "rua": "Rua São Marcelo",
            "numero": 12,
            "provedor": "Casas Bahia",
            "telefone": "71984287792"
        }

        response = self.client.post(url_create_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        anuncio_id = response['id']

        url_change_status = reverse('loja.anuncio-change-status', kwargs={
            'pk': anuncio_id
        })

        data = {
            'vendendo': False
        }
        response = self.client.patch(url_change_status, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['vendendo'], False)

        data = {
            'vendendo': True,
            'views': 12
        }
        response = self.client.patch(url_change_status, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['vendendo'], True)

        # Verifica se alterou o número de visualizações
        url_get_anuncio = reverse("loja.get-anuncio", kwargs={
            'pk': anuncio_id
        })
        response = self.client.get(url_get_anuncio)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content.decode('utf-8'))
        self.assertNotEqual(response['views'], data['views'])

        # Editar anúncio com outro usuário
        self.logout_loja()

        url_register_user = reverse('loja.register')

        data = {
            'email': 'teste@teste.com',
            'password': '12345678',
            'username': 'teste2',
            'account_type': 1
        }

        response = self.client.post(url_register_user, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.login_loja('teste2', '12345678')

        data = {
            'vendendo': False
        }
        response = self.client.patch(url_change_status, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_anuncio(self):
        self.login_loja()

        anuncio = Anuncio.objects.first()

        data = {
            'id_anuncio': anuncio.pk
        }
        response = self.client.post(url_favorite_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response['id_anuncio'], data["id_anuncio"])
        id_favorito = response['id']

        data = {}
        response = self.client.post(url_favorite_anuncio, data, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url_delete_favorite_anuncio = reverse('loja.delete-favorite-anuncio', kwargs={
            'pk': id_favorito
        })
        response = self.client.delete(url_delete_favorite_anuncio, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
