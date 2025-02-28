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
        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste',
            'password': 'secret'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']
        # Fim do login
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
            'Authorization': f'Bearer {token}'
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
        url_logout = reverse("knox_logout")
        self.client.post(url_logout, headers={
            'Authorization': f'Bearer {token}'
        })
        # Fim logout

        # Faz login no sistema
        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste 2',
            'password': 'secret2'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']
        # Fim do login

        response = self.client.put(url, data, headers={
            'Authorization': f'Bearer {token}'
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

        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste 2',
            'password': 'secret2'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']

        response = self.client.delete(url, headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url_logout = reverse("knox_logout")
        self.client.post(url_logout, headers={
            'Authorization': f'Bearer {token}'
        })

        data_login = {
            'username': 'teste',
            'password': 'secret'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']

        response = self.client.delete(url, headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_anuncio(self):
        anuncio = Anuncio.objects.first()
        url = reverse("loja.edit-anuncio", kwargs={"pk": anuncio.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # self.client.login(username="teste", password="secret")
        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste',
            'password': 'secret'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']

        response = self.client.get(url, headers={
            'Authorization': f'Bearer {token}'
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

        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste2',
            'password': 'secret2'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']

        response = self.client.get(url, headers={
            'Authorization': f'Bearer {token}'
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
        url_login = reverse("knox_login")
        data_login = {
            'username': 'teste',
            'password': 'secret'
        }

        response_login = self.client.post(url_login, data_login)
        response_login = json.loads(response_login.content.decode('utf-8'))
        token = response_login['token']

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
            'Authorization': f'Bearer {token}'
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
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content.decode('utf-8'))
