from rest_framework import serializers
from rest_framework.reverse import reverse

from . import models


class SupportsField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        pass


class AttestationSerializer(serializers.HyperlinkedModelSerializer):
    source_document = serializers.HyperlinkedRelatedField(read_only=True, view_name='api:source-document-detail')

    class Meta:
        model = models.Attestation
        fields = ('source_document',)


class SourceDocumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:source-document-type-detail')

    class Meta:
        model = models.SourceDocumentType
        fields = ('url', 'id', 'label')


class SourceDocumentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:source-document-detail')
    type = serializers.PrimaryKeyRelatedField(queryset=models.SourceDocumentType.objects.all())
    attestations = AttestationSerializer(read_only=True, many=True)

    class Meta:
        model = models.SourceDocument
        fields = ('url', 'id', 'attestations', 'identity', 'type', 'label')


class Attestable(serializers.Serializer):
    attestations = AttestationSerializer(many=True, required=False)


class AttestableSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            '@type': type(instance).__name__,
            'id': instance.pk,
            'url': reverse('api:{}-detail'.format(instance._meta.object_name.lower()),
                           kwargs={'pk': instance.pk},
                           request=self.context['request']),
            'label': str(instance),
        }
