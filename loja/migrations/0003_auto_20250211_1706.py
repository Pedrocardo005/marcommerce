# Generated by Django 4.2.7 on 2025-02-11 20:06

from django.conf import settings
from django.db import migrations


def populate_subcategorias(apps, schema_editor):
    Categoria = apps.get_model('loja', 'Categoria')
    SubCategoria = apps.get_model('loja', 'SubCategoria')
    CategoriaTranslation = apps.get_model('loja', 'CategoriaTranslation')

    subcategories = {
        'Aulas e Cursos': ['Tutoria', 'Educação continuada', 'Aulas de dança', 'Cursos de esportes', 'Música e canto', 'Design de arte',
                           'Cozinhar assados', 'Esotérico e Espiritual', 'Cursos de informática', 'Beleza', 'Cursos de idiomas', 'Mais'],
        'Animais': ['Cães e acessórios', 'Mais', 'Aves e Acessórios', 'Animais desaparecidos', 'Cuidado e treinamento de animais',
                    'Cavalos e Acessórios', 'Pequenos animais e acessórios', 'Peixes e Acessórios', 'Gatos e acessórios',
                    'Répteis e acessórios'],
        'Doação e trocas': ['Emprestar', 'Para trocar', 'Para doar'],
        'Música, Cinema e Livros': ['Livros e revistas', 'Filme e DVD', 'Escritório e papelaria', 'Histórias em quadrinhos',
                                    'Livros especializados, escola e estudos', 'Música e CDs', 'Instrumentos musicais', 'Adicional'],
        'Lazer, Hobby e Diversão': ['Arte e antiguidades', 'Perdidos e Achados', 'Lixo e caixas', 'Esportes e acampamento', 'Serviços de viagens e eventos',
                                    'Modelagem', 'Artesanato, artesanato e artes e ofícios', 'Amigos e parceiros de lazer', 'Comer Beber',
                                    'Esotérico e Espiritual', 'Coletar', 'Adicional'],
        'Shows e Ingressos': ['Comédia e Cabaré', 'Esportes', 'Crianças', 'Clássico e Cultura', 'Mais', 'Concertos'],
        'Empregos': [],
        'Multimídia e Eletrônica': ['Telemóveis e telecomunicações', 'Adicional', 'TV e vídeo', 'PC', 'Acessórios e software para PC', 'Jogos de vídeo e PC',
                                    'Cadernos', 'Consoles', 'Foto', 'Escritório, TI e serviços de TI', 'Áudio e Wi-fi', 'Eletrodomésticos', 'Tablets e leitores'],
        'Família, Criança e Bebê': ['Roupas para bebês e crianças', 'Brinquedo', 'Móveis de quarto infantil', 'Carrinhos', 'Assentos de bebê e cadeiras de criança',
                                    'Equipamento para bebês', 'Calçados para bebês e crianças', 'Cuidados com idosos', 'Babá e cuidado infantil', 'Adicional'],
        'Moda e Beleza': ['Acessórios e joias', 'Roupas femininas', 'Beleza'],
        'Casa e Jardim': ['Quarto', 'Serviços em casa e jardim', 'Lâmpadas e luz', 'Cozinha e sala de jantar', 'Faça você mesmo', 'Têxteis do lar',
                          'Jardim e plantas', 'Decoração', 'Escritório', 'Banheiro', 'Sala de estar', 'Adicional'],
        'Imóveis e Casas': ['Compre um apartamento', 'Compre uma casa', 'Imóveis comerciais', 'Mudanças e transporte', 'Alugar uma casa', 'Terreno e jardim',
                            'Garagem e arrecadação', 'Apartamentos e casas de férias', 'Em caráter temporário e apartamento compartilhado', 'Alugar um apartamento',
                            'Adicional'],
        'Carros e Motocicletas': ['Carros', 'Barcos e acessórios para barcos', 'Reparos e serviços', 'Caravanas e casas móveis', 'Peças automotivas e pneus', 'Ciclos',
                                  'Reboques e veículos comerciais', 'Motocicletas e peças', 'Scooters e peças', 'Lambreta']
    }

    for categoria in Categoria.objects.all():
        objeto = CategoriaTranslation.objects.filter(master_id=categoria.pk)
        categoria_pt = objeto.get(language_code=settings.LANGUAGE_CODE)

        sub_names = subcategories[categoria_pt.nome]

        for name in sub_names:
            subcategoria = SubCategoria()
            subcategoria._current_language = 'pt'
            subcategoria.name = name
            subcategoria.categoria = categoria
            subcategoria.save()


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_auto_20250211_1703'),
    ]

    operations = [
        migrations.RunPython(populate_subcategorias)
    ]
