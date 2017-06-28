from functools import singledispatch
from rest_framework import serializers
from rest_framework.relations import RelatedField
from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError, ModelSerializer

from . import models


class TypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = type(instance).__name__
        return data


class IdentityRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        assert isinstance(value, models.IdentityBase)
        return {'id': value.pk,
                '@type': type(value).__name__,
                'label': value.label}

    def get_queryset(self):
        return []

    def to_internal_value(self, data):
        if isinstance(data, str):
            return models.Identity.objects.get(id=data).identity
        raise ValidationError


class InvertedBooleanField(serializers.BooleanField):
    def to_internal_value(self, data):
        return not super().to_internal_value(data)

    def to_representation(self, value):
        return not super().to_representation(value)


class TerseIdentitySerializer(RelatedField):
    @singledispatch
    def to_representation(self, value):
        return {'id': value.id,
                'label': value.label,
                'qualified_label': value.label,
                'state': value.state}


class RelatedIdentitySerializer(RelatedField):
    def to_representation(self, value):
        return related_identity_to_representation(value, self.context)


@singledispatch
def related_identity_to_representation(identity, context):
    return {'id': identity.id,
            'label': identity.label,
            'qualified_label': identity.label,
            'state': identity.state,
            '@type': type(identity).__name__}


class IdentitySerializer(HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:identity-detail')
    id = serializers.UUIDField(read_only=True)
    identity = RelatedIdentitySerializer(read_only=True)

    class Meta:
        model = models.Identity

        fields = ('url', 'id', 'identity')
