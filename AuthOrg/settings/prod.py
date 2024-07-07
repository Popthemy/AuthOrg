import os
from .common import *



SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['vercel.app',".now.sh"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# for postgres offline
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': 'pg-leegreen-horluwatemilorunolamilekan-cb73.k.aivencloud.com',
        'PORT': '20755',
    }
}
