from dotenv import load_dotenv

load_dotenv()

from marcommerce.settings.base import *

# Override base.py settings here

DEBUG = True

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
