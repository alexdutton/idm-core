from rest_framework.relations import HyperlinkedIdentityField

from idm_core.identity.serializers import IdentitySerializer

from . import models


class ApplicationSerializer(IdentitySerializer):
    url = HyperlinkedIdentityField(view_name='api:application-detail')

    class Meta(IdentitySerializer.Meta):
        model = models.Application