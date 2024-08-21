from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from loja.models import Categoria


class CategoriaTestCase(TestCase):
    def setUp(self):
        c = Categoria()
        c.set_current_language('pt')
        c.nome = 'Categoria teste 1'
        c.icone = 'teste 1'
        c.save()

    def test_categoria_translation(self):
        # Translated é o novo filter
        categoria = Categoria.objects.translated(
            nome='Categoria teste 1').first()
        self.assertIsNotNone(categoria)
        self.assertEquals(categoria.icone, 'teste 1')

    def test_categoria_view(self):
        url_view = reverse('categories')

        response = self.client.get(url_view)
        self.assertTemplateUsed(response, 'loja/categoria_list.html')

        Categoria.objects.all().delete()

        response = self.client.get(url_view)
        self.assertTemplateUsed(response, 'loja/categoria_list.html')

    def test_login_user(self):
        url_login = reverse('loja.login')

        response = self.client.get(url_login)

        self.assertTemplateUsed(response, 'login.html')

        new_user = User()
        new_user.username = 'testerum'
        new_user.set_password('12345678')
        new_user.save()

        data = {
            'username': 'testerum',
            'password': '12345678'
        }

        response = self.client.post(url_login, data)

        self.assertRedirects(response, '/pt/')

        data = {
            'password': '12345678'
        }

        response = self.client.post(url_login, data)

        self.assertEquals(response.status_code, 500)

    # Testa logout com redirect para o index
    def test_logout_user_with_redirect(self):
        url_login = reverse('loja.login')
        url_logout = reverse('loja.logout')

        response = self.client.get(url_login)

        self.assertTemplateUsed(response, 'login.html')

        new_user = User()
        new_user.username = 'testerum'
        new_user.set_password('12345678')
        new_user.save()

        data = {
            'username': 'testerum',
            'password': '12345678'
        }

        response = self.client.post(url_login, data)

        self.assertRedirects(response, '/pt/')

        response = self.client.get(url_login)

        self.assertRedirects(response, '/pt/')

        response = self.client.post(url_logout)

        self.assertTemplateUsed(response, 'loja/usuario/logout.html')

        response = self.client.get(url_login)

        self.assertTemplateUsed(response, 'login.html')
