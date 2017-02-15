"""
Production Configurations

"""

from .common import *
# some variables, must be all capitals
APPNAME = 'HomeLetter'
APPVERSION = '0.0.1'

DEBUG = False

# define app mode
APP_MODE = 'production'

# set this to allow use "if debug" in template
INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1',
)

# message level
MESSAGE_LEVEL = 10  # DEBUG



