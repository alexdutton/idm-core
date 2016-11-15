from rest_framework import serializers
from rest_framework.reverse import reverse

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


class AttestableSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            '@type': type(instance).__name__,
            'id': instance.pk,
            'url': reverse('{}-detail'.format(instance._meta.object_name.lower()),
                           kwargs={'pk': instance.pk},
                           request=self.context['request']),
            'label': str(instance),
        }
