# Generated by Django 4.2.7 on 2023-12-14 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0012_produto_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtotranslation',
            name='descricao',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]