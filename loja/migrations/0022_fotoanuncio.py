# Generated by Django 4.2.7 on 2025-02-01 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0021_alter_anuncio_data_venda'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotoAnuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField()),
                ('url_imagem', models.TextField()),
                ('anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='loja.anuncio')),
            ],
        ),
    ]
