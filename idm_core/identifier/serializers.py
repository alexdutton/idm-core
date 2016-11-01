from rest_framework import serializers

from idm_core.attestation.serializers import Attestable
from . import models


class IdentifierTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.IdentifierType


class IdentifierSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=models.IdentifierType.objects.all())

    class Meta:
        model = models.Identifier


class EmbeddedIdentifierSerializer(IdentifierSerializer):
    identity = serializers.CharField(required=False, source='identity_id', write_only=True)

    class Meta(IdentifierSerializer.Meta):
        exclude = ('attestations',)
