# Generated by Django 4.2.7 on 2025-02-23 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0006_alter_customuser_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotoanuncio',
            name='imagem',
            field=models.ImageField(null=True, upload_to='pictures/'),
        ),
    ]
