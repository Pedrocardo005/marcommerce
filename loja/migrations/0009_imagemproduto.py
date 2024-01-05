# Generated by Django 4.2.7 on 2023-11-24 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0008_endereco_produto_endereco'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('imagem', models.ImageField(upload_to=None, verbose_name='')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='loja.produto')),
            ],
        ),
    ]