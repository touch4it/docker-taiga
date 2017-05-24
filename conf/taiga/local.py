# Please modify this file as needed, see the local.py.example for details:
# https://github.com/taigaio/taiga-back/blob/master/settings/local.py.example

# Importing common provides default settings, see:
# https://github.com/taigaio/taiga-back/blob/master/settings/common.py
from .common import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('TAIGA_DB_NAME', 'taiga'),
        'HOST': os.getenv('TAIGA_DB_HOST', 'postgres'),
        'USER': os.getenv('TAIGA_DB_USER', 'taiga'),
        'PASSWORD': os.getenv('TAIGA_DB_PASSWORD', 'taiga')
    }
}

TAIGA_HOSTNAME = os.getenv('TAIGA_HOSTNAME', 'localhost')

SITES['api']['domain'] = TAIGA_HOSTNAME
SITES['front']['domain'] = TAIGA_HOSTNAME

MEDIA_URL = 'http://' + TAIGA_HOSTNAME + '/media/'
STATIC_URL = 'http://' + TAIGA_HOSTNAME + '/static/'

if os.getenv('TAIGA_SSL', 'false').lower() == 'true':
    SITES['api']['scheme'] = 'https'
    SITES['front']['scheme'] = 'https'

    MEDIA_URL = 'https://' + TAIGA_HOSTNAME + '/media/'
    STATIC_URL = 'https://' + TAIGA_HOSTNAME + '/static/'

SECRET_KEY = os.getenv('TAIGA_SECRET_KEY', 'mysecret')

if os.getenv('TAIGA_CELERY_ENABLED', 'false').lower() == 'true':
    CELERY_ENABLED = True

if os.getenv('TAIGA_EVENTS_ENABLED', 'false').lower() == 'true':
    EVENTS_PUSH_BACKEND = os.getenv('TAIGA_EVENTS_PUSH_BACKEND', 'taiga.events.backends.rabbitmq.EventsPushBackend')
    EVENTS_PUSH_BACKEND_OPTIONS = {
        'url': os.getenv('TAIGA_EVENTS_PUSH_BACKEND_URL', 'amqp://guest:guest@rabbit:5672//')
    }

if os.getenv('TAIGA_EMAIL_ENABLED', 'false').lower() == 'true':
    DEFAULT_FROM_EMAIL = os.getenv('TAIGA_EMAIL_ADDR')
    CHANGE_NOTIFICATIONS_MIN_INTERVAL = 300  # in seconds

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = os.getenv('TAIGA_EMAIL_HOST', 'localhost')
    EMAIL_PORT = int(os.getenv('TAIGA_EMAIL_PORT', 25))
    EMAIL_HOST_USER = os.getenv('TAIGA_EMAIL_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('TAIGA_EMAIL_PASS', '')
    EMAIL_USE_TLS = os.getenv('TAIGA_EMAIL_USE_TLS', 'false').lower() == 'true'

PUBLIC_REGISTER_ENABLED = os.getenv('TAIGA_PUBLIC_REGISTER_ENABLED', 'false').lower() == 'true'
DEBUG = os.getenv('TAIGA_DEBUG', 'false').lower() == 'true'
TEMPLATE_DEBUG = os.getenv('TAIGA_TEMPLATE_DEBUG', 'false').lower() == 'true'
