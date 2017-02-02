"""
Local settings

- Run in Debug mode

"""
# from django.conf.locale.en import formats as en_formats
from .common import *

# some variables, must be all capitals
APPNAME = 'HomeLetter'
APPVERSION = '0.0.1'

# define app mode
APP_MODE = 'local'

# set this to allow use "if debug" in template
INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1',
)

# message level
MESSAGE_LEVEL = 10  # DEBUG

# en_formats.DATE_FORMAT = "d-m-Y"

# uncomment below to before deploying the application
# ALLOWED_HOSTS = ['*']
# DEBUG = False
