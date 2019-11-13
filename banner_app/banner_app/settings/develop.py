from .base import *


SECRET_KEY = '=!e0lr$&cx8@9%8^*7a-c6i*2+%xqoyr^-0fz7m@6&qm(z!*uv'
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'banner_database',
        'USER': 'py_dev',
        'PASSWORD': 'panta1494',
        'HOST': 'localhost',
        'PORT': '',
    }
}
