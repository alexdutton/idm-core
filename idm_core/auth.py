from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.backends import RemoteUserBackend as BaseRemoteUserBackend
from django.core.exceptions import PermissionDenied
from rest_framework.authentication import BaseAuthentication

from idm_core.identity.models import Identity


class RemoteUserBackend(BaseRemoteUserBackend):
    create_unknown_user = False

    def clean_username(self, username):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(principal_name=username)
        except UserModel.DoesNotExist:
            raise PermissionDenied
        else:
            return getattr(user, UserModel.USERNAME_FIELD)


class RemoteUserAuthentication(BaseAuthentication):
    """
    REMOTE_USER authentication.

    To use this, set up your web server to perform authentication, which will
    set the REMOTE_USER environment variable. You will need to have
    'django.contrib.auth.backends.RemoteUserBackend in your
    AUTHENTICATION_BACKENDS setting
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def authenticate(self, request):
        user = authenticate(remote_user=request.META.get(self.header))
        if user and user.is_active:
            return user, None


def process_userinfo(user, claims):
    identity = Identity.objects.get(id=claims['identity_id'])
    user.identity_id = identity.id
    user.identity_content_type_id = identity.content_type_id
    user.save()