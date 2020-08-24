from .settings import *
from decouple import config, Csv
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'museakad_production',
        'USER': 'museakad_prod',
        'PASSWORD': 'digistar_muse23',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    }
}