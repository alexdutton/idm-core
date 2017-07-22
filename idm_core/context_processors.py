from django.conf import settings


def idm_core(request):
    return {
        'IDM_AUTH_URL': settings.IDM_AUTH_URL,
    }
