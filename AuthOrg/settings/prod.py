import os
from .common import *


DEBUG = True


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['localhost','127.0.0.1','auth-org.vercel.app/']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# for postgres online
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'defaultdb',
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '20755',
    }
}
