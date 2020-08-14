from .settings import *
from decouple import config, Csv
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_prod.sqlite3'),
    }
}