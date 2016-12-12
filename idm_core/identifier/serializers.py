from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from idm_core.attestation.serializers import Attestable
from . import models


class IdentifierTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.IdentifierType


class IdentifierSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=models.IdentifierType.objects.all())

    def create(self, validated_data):
        print(validated_data)
        if validated_data['identity'].type not in validated_data['type'].applicable_to.all():
            raise ValidationError("Identifier type '{}' not applicable to identity type '{}'".format(
                validated_data['type'].id,
                validated_data['identity'].type.id))
        return super().create(validated_data)

    class Meta:
        model = models.Identifier

        fields = ('type', 'value', 'identity', 'attestations')
        read_only_fields = ('identity', 'type')


class EmbeddedIdentifierSerializer(IdentifierSerializer):
    identity = serializers.CharField(required=False, source='person_id', write_only=True)

    class Meta(IdentifierSerializer.Meta):
        fields = ('type', 'value', 'identity')
