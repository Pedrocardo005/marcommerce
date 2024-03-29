# Generated by Django 4.0.9 on 2023-02-27 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0007_produtoview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bairro', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='endereco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='loja.endereco'),
        ),
    ]
