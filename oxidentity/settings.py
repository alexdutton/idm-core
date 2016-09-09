import email

import django
import os
from celery.schedules import crontab

DEBUG = os.environ.get('DJANGO_DEBUG')

USE_TZ = True
TIME_ZONE = 'Europe/London'


ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split() if not DEBUG else ['*']

try:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
except KeyError:
    if DEBUG:
        SECRET_KEY = 'very secret key'
    else:
        raise

if 'DJANGO_ADMINS' in os.environ:
    ADMINS = [email.utils.parseaddr(addr.strip()) for addr in os.environ['DJANGO_ADMINS'].split(',')]

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'oxidentity'),
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'oxidentity',
    'oxidentity.org_relationship',
    'oxidentity.attestation',
    'oxidentity.gender',
    'oxidentity.identifier',
    'oxidentity.name',
    'oxidentity.nationality',
    'oxidentity.delayed_save',
    'rest_framework',
    'reversion',
]
try:
    __import__('django_extensions')
except ImportError:
    pass
else:
    INSTALLED_APPS.append('django_extensions')

MIDDLEWARE_CLASSES = [
    #'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

]

ROOT_URLCONF = 'oxidentity.urls'

STATIC_URL = '/static/'

API_BASE = os.environ.get('API_BASE', 'http://localhost:8000/')

# AMQP
BROKER_URL = os.environ.get('AMQP_BROKER_URL', 'amqp://guest:guest@localhost/')

CELERYBEAT_SCHEDULE = {
    'delayed-save': {
        'task': 'oxidentity.delayed_save.tasks.schedule_impending_saves',
        'schedule': crontab(),
    }
}