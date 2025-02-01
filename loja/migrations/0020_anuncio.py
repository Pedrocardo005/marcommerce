# Generated by Django 4.2.7 on 2025-02-01 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0019_marcaarte'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_expirar', models.DateTimeField()),
                ('ativo', models.BooleanField()),
                ('views', models.IntegerField()),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('condicao', models.CharField(choices=[('SH', 'Second hand'), ('N', 'New'), ('RB', 'Refurbished')], max_length=2)),
                ('envio', models.IntegerField(choices=[(1, 'DHL'), (2, 'Hermes envio'), (3, 'DPD'), (4, 'GLS'), (5, 'UPS'), (6, 'TNT'), (7, 'Outro')])),
                ('cidade', models.CharField(max_length=255)),
                ('rua', models.CharField(max_length=255)),
                ('numero', models.IntegerField()),
                ('vendendo', models.BooleanField(default=True)),
                ('tipo_oferta', models.IntegerField(choices=[(1, 'Preço fixo'), (2, 'Base para negociação'), (3, 'Sob demanda'), (4, 'Para dar de presente')])),
                ('provedor', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=255)),
                ('data_venda', models.DateTimeField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='anuncios', to='loja.categoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='anuncios', to='loja.customuser')),
            ],
        ),
    ]
