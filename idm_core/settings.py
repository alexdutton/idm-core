import email
import logging

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
    'camera_imagefield',
    'celery_haystack',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'haystack',
    'idm_brand',
    'idm_core',
    'idm_core.application.apps.ApplicationConfig',
    'idm_core.attestation.apps.AttestationConfig',
    'idm_core.identity.apps.IdentityConfig',
    'idm_core.contact',
    'idm_core.course',
    'idm_core.relationship.apps.OrgRelationshipConfig',
    'idm_core.identifier.apps.IdentifierConfig',
    'idm_core.image',
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
    'widget_tweaks',
]
try:
    __import__('django_extensions')
except ImportError:
    pass
else:
    INSTALLED_APPS.append('django_extensions')

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    #  'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'oidc_auth.auth.OpenIDConnectBackend',
    'django.contrib.auth.backends.ModelBackend',
    'idm_core.auth.RemoteUserBackend',
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

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'idm_core.context_processors.idm_core',
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
BROKER_HOSTNAME = os.environ.get('BROKER_HOSTNAME', 'localhost')
BROKER_SSL = os.environ.get('BROKER_SSL', 'yes').lower() not in ('no', '0', 'off', 'false')
BROKER_VHOST = os.environ.get('BROKER_VHOST', '/')
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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': os.environ.get('HAYSTACK_SOLR_URL', 'http://127.0.0.1:8983/solr'),
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'


OIDC_AUTH = {
    'DEFAULT_PROVIDER': {
        'issuer': os.environ.get('OIDC_ISSUER', 'http://localhost:8001/'),
        'authorization_endpoint': os.environ.get('OIDC_AUTHORIZATION_ENDPOINT',
                                                 'http://localhost:8001/openid/authorize'),
        'token_endpoint': os.environ.get('OIDC_TOKEN_ENDPOINT', 'http://localhost:8001/openid/token'),
        'userinfo_endpoint': os.environ.get('OIDC_USERINFO_ENDPOINT', 'http://localhost:8001/openid/userinfo'),
        'jwks_uri': os.environ.get('OIDC_JWKS_URI', 'http://localhost:8001/openid/jwks'),
        'client_id': os.environ.get('OIDC_CLIENT_ID', ''),
        'client_secret': os.environ.get('OIDC_CLIENT_SECRET', ''),
        'signing_alg': os.environ.get('OIDC_SIGNING_ALG', 'RS256')
    },
    'SCOPES': os.environ.get('OIDC_SCOPES', 'identity').split(),
    'PROCESS_USERINFO': 'idm_core.auth.process_userinfo',
}

IDM_BROKER = {
    'CONSUMERS': [{
        'queues': [kombu.Queue('idm.core.user',
                               exchange=kombu.Exchange('idm.auth.user', type='topic', passive=True),
                               routing_key='#')],
        'tasks': ['idm_core.tasks.update_user'],
    }],
}

SESSION_COOKIE_NAME = 'idm-core-sessionid'

LOGIN_URL = 'oidc-login'
LOGOUT_URL = 'logout'

l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())

EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'idm_core.auth.RemoteUserAuthentication',
        'drf_negotiate.authentication.NegotiateAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
}

IDM_AUTH_URL = os.environ.get('IDM_AUTH_URL', 'http://localhost:8001/')
IDM_CARD_URL = os.environ.get('IDM_CARD_URL', 'http://localhost:8002/')
IDM_AUTH_API_URL = os.environ.get('IDM_AUTH_API_URL', 'http://localhost:8001/api/')

# Allow request bodies up to 2 MiB, so people can upload photos and document scans
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024**3

SENDFILE_BACKEND = os.environ.get('SENDFILE_BACKEND', 'sendfile.backends.development')
