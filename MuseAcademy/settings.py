"""
Django settings for MuseAcademy project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import sys
import django_heroku
import dj_database_url
from decouple import config, Csv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR               = os.path.join(BASE_DIR,'templates')
STATIC_DIR                  = os.path.join(BASE_DIR,'static')
MEDIA_DIR                   = os.path.join(BASE_DIR,'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS   = config('ALLOWED_HOSTS', cast=Csv())
DEBUG           = config('DEBUG', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.forms',
    # APPS
    'core',
    'apps.api',
    'apps.user',
    'apps.mentor',
    'apps.app',
    'apps.payment',
    'apps.management',
    # TOOLS
    'phonenumber_field',
    # 'livereload',
    'croppie',
    'django_crontab',
    'rest_framework',
    'widget_tweaks',
    'social_django',
    'tempus_dominus',
    'django_summernote',
    'crequest',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware', # User prefered languange

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'MuseAcademy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'MuseAcademy.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# SOCIAL AUTH
AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',

    'core.custom_authentication.EmailOrUsernameModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'url_you_want'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY      = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET   = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'core.pipeline.save_profile',  # <--- set the path to the function
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# SOCIAL AUTH

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# ATOMIC_REQUESTS = True

# CRONJOBS = [
#     ('1 * * * *', 'core.cron.periodic_task')
# ]
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'id'

LANGUAGES = [
    ('id', 'Indonesia'), 
    ('en', 'English'), 
    ('ja', 'Japanese'),
    # ('ja', _('Japanese')),
]


TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS    = [STATIC_DIR,]
STATIC_ROOT         = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL          = '/static/'

# root media directory and url

MEDIA_ROOT          = MEDIA_DIR
MEDIA_URL           = '/media/'

PROTECTED_MEDIA_ROOT    = os.path.join(BASE_DIR,'protected_media')
PROTECTED_MEDIA_URL     = "/protected_media/"

# Login url and redirect login url
LOGIN_URL           = '/login/'
LOGIN_REDIRECT_URL  = '/profile/'
LOGOUT_URL          = '/logout'

# custom user model django
AUTH_USER_MODEL = 'core.User'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# MIDTRANS
MIDTRANS_SERVER_KEY=config('MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY=config('MIDTRANS_CLIENT_KEY')

# Email Server
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST          = config('EMAIL_HOST')
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT          = config('EMAIL_PORT', cast=int)

SUMMERNOTE_CONFIG = {
    'iframe': True,
    # 'summernote': {
    #     'width': '100%',
    #     'height': '400px',
    #     'toolbar': [
    #         ['style', ['style']],
    #         ['font', ['bold', 'underline', 'clear']],
    #         ['fontname', ['fontname']],
    #         ['color', ['color']],
    #         ['para', ['ul', 'ol', 'paragraph']],
    #         ['table', ['table']],
    #         ['insert', ['link', 'picture', 'video']],
    #         ['view', ['fullscreen', 'codeview', 'help']],
    #     ],
    # },
    'summernote': {
        'width': '100%',
        'height': '400px',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },
    'js': (
        # '/static/summernote-ext-print.js',
    ),
    'js_for_inplace': (
        # '/static/summernote-ext-print.js',
    ),
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
    ),
    'css_for_inplace': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.40.0/theme/base16-dark.min.css',
    ),
    'codemirror': {
        'theme': 'base16-dark',
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
    },
    'lazy': False,
}

PAGINATE_DEFAULT    = 10 
NILAI_SKM           = 75

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

django_heroku.settings(locals())
