from marcommerce.settings.base import *
from marcommerce.settings.others_config import *

# Override base.py settings here

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

DEBUG = True
