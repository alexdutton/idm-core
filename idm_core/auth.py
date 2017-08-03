from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend as BaseRemoteUserBackend
from django.core.exceptions import PermissionDenied

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


def process_userinfo(user, claims):
    identity = Identity.objects.get(id=claims['identity_id'])
    user.identity_id = identity.id
    user.identity_content_type_id = identity.content_type_id
    user.save()