"""
Production Configurations

"""

from .common import *
# some variables, must be all capitals
APPNAME = 'HomeLetter'
APPVERSION = '0.0.1'

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'homeletter',
        'USER': 'homeletter',
        'PASSWORD': '9fZ8Z2KbTd8kkBkf',
        'HOST': '192.168.178.40',
        'PORT': '3306',
    }
}


DEBUG = False

# define app mode
APP_MODE = 'production'

ALLOWED_HOSTS = ['*']

# message level
MESSAGE_LEVEL = 10  # DEBUG



