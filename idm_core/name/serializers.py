from rest_framework import serializers

from idm_core.attestation.serializers import Attestable
from idm_core.name.models import NameContext
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

        fields = ('person', 'plain', 'plain_full', 'marked_up', 'familiar', 'sort', 'first', 'last', 'active',
                  'space_delimited', 'components', 'contexts', 'attestations')

        read_only_fields = (
            'person',
            'plain',
            'plain_full'
            'marked_up',
            'familiar',
            'sort',
            'first',
            'last'
        )


class EmbeddedNameSerializer(NameSerializer):
    person = serializers.CharField(required=False, source='person_id', write_only=True)

    class Meta(NameSerializer.Meta):
        fields = tuple(set(NameSerializer.Meta.fields) - {'attestations'})
