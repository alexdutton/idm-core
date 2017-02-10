from idm_core.identity.serializers import IdentitySerializer

from . import models


class ApplicationSerializer(IdentitySerializer):
    class Meta(IdentitySerializer.Meta):
        model = models.Application