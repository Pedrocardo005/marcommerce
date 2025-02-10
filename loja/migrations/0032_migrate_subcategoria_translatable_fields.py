from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def populate_subcategorias(apps, schema_editor):
    SubCategoria = apps.get_model('loja', 'SubCategoria')
    SubCategoriaTranslation = apps.get_model('loja', 'SubCategoriaTranslation')

    for subcategoria in SubCategoria.objects.all():
        sub_translated = SubCategoriaTranslation()
        sub_translated.master_id = subcategoria.pk
        sub_translated.language_code = settings.LANGUAGE_CODE
        sub_translated.name = subcategoria.nome
        sub_translated._parler_meta = []
        sub_translated.save()


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0031_subcategoriatranslation'),
    ]

    operations = [
        migrations.RunPython(populate_subcategorias),
    ]
