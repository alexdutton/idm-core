from rest_framework import serializers

from idm_identity.attestation.serializers import Attestable
from idm_identity.name.models import NameContext
from . import models


class NameSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    contexts = serializers.PrimaryKeyRelatedField(queryset=NameContext.objects.all(), many=True)

    # def create(self, validated_data):
    #     components = validated_data.pop('components')
    #     name = super(NameSerializer, self).create(validated_data)
    #     for i, component in enumerate(components):
    #         component.update({'name': name, 'order': i})
    #     self.fields['components'].create(components)
    #     return name

    class Meta:
        model = models.Name

        read_only_fields = (
            'plain',
            'marked_up',
            'familiar',
        )

class EmbeddedNameSerializer(NameSerializer):
    identity = serializers.CharField(required=False, source='identity_id', write_only=True)

    class Meta(NameSerializer.Meta):
        exclude = ('attestations',)
