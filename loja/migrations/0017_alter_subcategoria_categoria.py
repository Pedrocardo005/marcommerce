# Generated by Django 4.2.7 on 2024-07-27 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0016_auto_20240717_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategoria',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='loja.categoria'),
        ),
    ]