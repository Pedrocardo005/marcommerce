# Generated by Django 4.2.7 on 2025-01-29 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0017_alter_subcategoria_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='categoria',
        ),
    ]
