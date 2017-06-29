from rest_framework import serializers

from idm_core.identity.serializers import IdentitySerializer

from . import models


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:application-detail')

    class Meta(IdentitySerializer.Meta):
        model = models.Application
        fields = ('url', 'id', 'label')