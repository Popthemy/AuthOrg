from .common import *
import os

SECRET_KEY = 'django-insecure-3*&1zonywsq1o$jz8@yda2k9mum&p-_(d5hpu4i1xn7htmgpm^'

DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# for postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Authorg',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('book hall postgres PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
