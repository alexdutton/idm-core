import email

import django
import kombu
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
    'idm_brand',
    'idm_core', #.apps.IDMCoreConfig',
    'idm_core.application.apps.ApplicationConfig',
    'idm_core.attestation.apps.AttestationConfig',
    'idm_core.identity.apps.IdentityConfig',
    'idm_core.contact',
    'idm_core.course',
    'idm_core.relationship.apps.OrgRelationshipConfig',
    'idm_core.identifier',
    'idm_core.name.apps.NameConfig',
    'idm_core.person.apps.PersonConfig',
    'idm_core.nationality.apps.NationalityConfig',
    'idm_core.delayed_save',
    'idm_core.organization.apps.OrganizationConfig',
    'idm_core.selfservice',
    'idm_broker.apps.IDMBrokerConfig',
    'oidc_auth',
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

AUTHENTICATION_BACKENDS = [
    'oidc_auth.auth.OpenIDConnectBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# OIDC_PROVIDERS = {
#     'idm-auth': {
#         "srv_discovery_url": "http://localhost:8001/openid/",
#         "behaviour": OIDC_DEFAULT_BEHAVIOUR,
#         "client_registration": {
#             "client_id": "your_client_id",
#             "client_secret": "your_client_secret",
#             "redirect_uris": ["http://localhost:8000/openid/callback/login/"],
#             "post_logout_redirect_uris": ["http://localhost:8000/openid/callback/logout/"],
#             "token_endpoint_auth_method": "client_secret_post",
#         }
#     }
# }

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
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')

API_BASE = os.environ.get('API_BASE', 'http://localhost:8000/')

CLAIM_URL = os.environ.get('CLAIM_URL', 'http://localhost:8001/claim/{}/')

# AMQP
BROKER_ENABLED = bool(os.environ.get('BROKER_ENABLED'))
BROKER_TRANSPORT = os.environ.get('BROKER_TRANSPORT', 'amqp')
BROKER_HOSTNAME= os.environ.get('BROKER_HOSTNAME', 'localhost')
BROKER_SSL = os.environ.get('BROKER_SSL', 'yes').lower() not in ('no', '0', 'off', 'false')
BROKER_VHOST= os.environ.get('BROKER_VHOST', '/')
BROKER_USERNAME = os.environ.get('BROKER_USERNAME', 'guest')
BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', 'guest')
BROKER_PREFIX = os.environ.get('BROKER_PREFIX', 'idm.core.')

AUTH_USER_MODEL = 'identity.User'

CELERYBEAT_SCHEDULE = {
    'delayed-save': {
        'task': 'idm_core.delayed_save.tasks.schedule_impending_saves',
        'schedule': crontab(),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'idm_core.pagination.StandardResultsSetPagination'
}

OIDC_AUTH = {
    'DEFAULT_PROVIDER': {
        'issuer': 'http://localhost:8001/',
        'authorization_endpoint': 'http://localhost:8001/openid/authorize',
        'token_endpoint': 'http://localhost:8001/openid/token',
        'userinfo_endpoint': 'http://localhost:8001/openid/userinfo',
        'jwks_uri': 'http://localhost:8001/openid/jwks',
        'client_id': '118661',
        'client_secret': '9a82e2c9b52fadd87ee79b67ead11a28012e270233432e1297c44665',
    },
    'SCOPES': ['identity'],
}

IDM_BROKER = {
    'CONSUMERS': [{
        'queues': [kombu.Queue('idm.identity.user',
                               exchange=kombu.Exchange('idm.auth.user', type='topic'),
                               routing_key='#')],
        'tasks': ['idm_core.tasks.update_user'],
    }],
}

SESSION_COOKIE_NAME = 'idm-core-sessionid'

import logging

LOGIN_URL = 'oidc-login'

l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('drf_negotiate.authentication.NegotiateAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
}