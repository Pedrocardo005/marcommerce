from marcommerce.settings.base import *
from marcommerce.settings.others_config import *

# Override base.py settings here

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': int(os.environ.setdefault('DATABASE_PORT', '5432')),
    }
}

DEBUG = True
