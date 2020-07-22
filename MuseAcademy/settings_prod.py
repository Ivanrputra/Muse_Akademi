from .settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}