from django.test import TestCase
from django.urls import reverse

from loja.models import Categoria


class CategoriaTestCase(TestCase):
    def setUp(self):
        c=Categoria()
        c.set_current_language('pt')
        c.nome='Categoria teste 1'
        c.icone='teste 1'
        c.save()

    def test_categoria_translation(self):
        # Translated é o novo filter
        categoria = Categoria.objects.translated(nome='Categoria teste 1').first()
        self.assertIsNotNone(categoria)
        self.assertEquals(categoria.icone, 'teste 1')

    def test_categoria_view(self):
        url_view = reverse('categories')
        
        response = self.client.get(url_view)
        self.assertTemplateUsed(response, 'categories.html')

        Categoria.objects.all().delete()

        response = self.client.get(url_view)
        self.assertTemplateUsed(response, 'categories.html')
