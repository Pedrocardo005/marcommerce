import os

from marcommerce.settings.base import *

# Armazenamento de informações

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL')
AWS_QUERYSTRING_AUTH = os.getenv('AWS_QUERYSTRING_AUTH')

DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE')

ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS')

CORS_ALLOWED_ORIGINS = ORIGINS.split(',')

# Envio de e-mail

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SITE_ID = os.getenv('SITE_ID')

# Banco de dados

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Outros

DEBUG = os.getenv('DEBUG')
