from rest_framework import serializers

from . import models


class SupportsField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        pass


class AttestationSerializer(serializers.HyperlinkedModelSerializer):
    supports = SupportsField(read_only=True)

    class Meta:
        model = models.Attestation
        exclude = ('supports_content_type', 'supports_object_id')


class SourceDocumentSerializer(serializers.HyperlinkedModelSerializer):
    attestations = AttestationSerializer(read_only=True, many=True)

    class Meta:
        model = models.SourceDocument


class Attestable(serializers.Serializer):
    attestations = AttestationSerializer(many=True, required=False)