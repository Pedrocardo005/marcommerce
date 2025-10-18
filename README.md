# MarCommerce

Projeto para criação de um ecommerce de exemplo.

## Ferramentas

Python 3.9.6

Django 4.2.20

Docker
 - (working 18-10-2025 28.5.1)

Docker Compose 
 - (working 18-10-2025 2.40.1)

AWS

S3

### Iniciando o projeto

1. Faça o clone do projeto no sua máquina com o comando:
```bash
git clone https://github.com/Pedrocardo005/marcommerce
```

2. Entre na pasta do projeto copiado:
```bash
cd marcommerce
```

3. Rode o banco de dados da aplicação com o docker-compose:
```bash
sudo make only-database
```

4. Crie um ambiente virtual:
```bash
python -m venv env
```

5. Ative o ambiente virtual:
```bash
source env/bin/activate
```

6. Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

7. Crie um arquivo `others_config.py` dentro da pasta marcommerce/settings.

8. Crie um super usuário:
```bash
python manage.py createsuperuser
```

9. Rode a aplicação:
```bash
python manage.py runserver
```

10. Aplique as migrações:
```bash
python manage.py migrate
```

### OBS

No arquivo de configurações, mais especificamente nas variáveis da aws, lembrar de trocar o texto e por informações corretas para se conectar ao serviço.

Elas são:
```python
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-region'  # e.g., us-east-1
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

Variáveis do envio de e-mail que precisam ser modificadas:
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
DEFAULT_FROM_EMAIL = "your@gmail.com"
SITE_ID = 1

FRONTEND_URL = ""
```

## Deploy no render

Com base no arquivo `.env.example` insira as variáveis de ambiente no ambiente render com os valores corretos.

## Rodar a aplicação assíncrona

É possível rodar a aplicação de forma assíncrona e com múltiplas threads. Só iniciar a aplicação com o seguinte comando:
```bash
uvicorn marcommerce.asgi:application --workers 6
```

O texto `--workers 6` indica que 6 threads serão usadas. Se desejar utilizar mais, modifique esse valor a sua preferência.
