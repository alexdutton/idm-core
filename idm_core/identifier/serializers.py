from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from idm_core.attestation.serializers import Attestable
from idm_core.identity.serializers import TerseIdentitySerializer
from . import models


class IdentifierTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.IdentifierType


class IdentifierSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=models.IdentifierType.objects.all())
    identity = TerseIdentitySerializer(read_only=True)

    def create(self, validated_data):
        identity_models = {ct.model_class() for ct in validated_data['type'].applicable_to.all()}
        if not validated_data['type'].applicable_to_all and type(validated_data['identity']) not in identity_models:
            raise ValidationError("Identifier type '{}' not applicable to identity type '{}'".format(
                validated_data['type'].id,
                validated_data['identity']._meta.label))
        return super().create(validated_data)

    class Meta:
        model = models.Identifier

        fields = ('type', 'value', 'identity', 'attestations')
        read_only_fields = ('identity', 'type')


class EmbeddedIdentifierSerializer(IdentifierSerializer):
    identity = serializers.Field(required=False, write_only=True)

    class Meta(IdentifierSerializer.Meta):
        fields = ('type', 'value', 'identity')


class IdentifiableSerializer(serializers.ModelSerializer):
    identifiers = EmbeddedIdentifierSerializer(many=True)
