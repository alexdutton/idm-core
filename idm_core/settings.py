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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'idm_core'),
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'idm_core.person.apps.PersonConfig',
    'idm_core.contact',
    'idm_core.org_relationship.apps.OrgRelationshipConfig',
    'idm_core.attestation',
    'idm_core.identifier',
    'idm_core.name',
    'idm_core.notification.apps.NotificationConfig',
    'idm_core.nationality',
    'idm_core.delayed_save',
    'idm_core.organization',
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
    'django.middleware.common.CommonMiddleware',
    #'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
            ),
        },
    },
]

ROOT_URLCONF = 'idm_core.urls'

STATIC_URL = '/static/'

API_BASE = os.environ.get('API_BASE', 'http://localhost:8000/')

CLAIM_URL = os.environ.get('CLAIM_URL', 'http://localhost:8001/claim/{}/')

# AMQP
BROKER_ENABLED = bool(os.environ.get('AMQP_BROKER_ENABLED'))
BROKER_TRANSPORT = os.environ.get('AMQP_BROKER_TRANSPORT', 'amqp')
BROKER_HOSTNAME= os.environ.get('AMQP_BROKER_HOSTNAME', 'localhost')
BROKER_VHOST= os.environ.get('AMQP_BROKER_VHOST', '/')
BROKER_USERNAME = os.environ.get('AMQP_BROKER_USERNAME', 'guest')
BROKER_PASSWORD = os.environ.get('AMQP_BROKER_PASSWORD', 'guest')
BROKER_PREFIX = os.environ.get('AMQP_BROKER_PREFIX', 'idm.core.')

CELERYBEAT_SCHEDULE = {
    'delayed-save': {
        'task': 'idm_core.delayed_save.tasks.schedule_impending_saves',
        'schedule': crontab(),
    }
}
