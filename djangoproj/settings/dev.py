from djangoproj.settings.base import *


SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'devDjangoDB',
    }
}


EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'

try:
    from djangoproj.settings.local import *
except:
    pass
