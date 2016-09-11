from rest_framework import serializers

from oxidentity.attestation.serializers import Attestable
from oxidentity.name.models import NameContext
from . import models


class NameComponentSerializer(serializers.ModelSerializer):
    name = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        super(NameComponentSerializer, self).create(validated_data)

    class Meta:
        model = models.NameComponent


class EmbeddedNameComponentSerializer(NameComponentSerializer):
    name = serializers.IntegerField(required=False, source='name_id', write_only=True)
    order = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = models.NameComponent
        exclude = ('id',)


class NameSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    components = EmbeddedNameComponentSerializer(many=True)
    contexts = serializers.PrimaryKeyRelatedField(queryset=NameContext.objects.all(), many=True)

    def create(self, validated_data):
        components = validated_data.pop('components')
        name = super(NameSerializer, self).create(validated_data)
        for i, component in enumerate(components):
            component.update({'name': name, 'order': i})
        self.fields['components'].create(components)
        return name

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
        exclude = ('components', 'attestations')
