# Generated by Django 4.2.7 on 2023-12-15 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0013_produtotranslation_descricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtotranslation',
            name='categoria',
        ),
        migrations.AddField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='loja.categoria'),
        ),
    ]
