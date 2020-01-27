from ssbear.settings import *

DEBUG = False
ALLOWED_HOSTS = ['www.ssbear.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ssbear',
        'USER': 'postgres',
        'PASSWORD': 'qwer1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



