# Generated by Django 4.2.7 on 2025-02-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0020_anuncio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='data_venda',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
