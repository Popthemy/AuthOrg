import os
from .common import *
import dj_database_url


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['vercel.app',".now.sh"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# for postgres offline
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}