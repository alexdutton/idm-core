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


class IdentitySerializer(HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = models.Identity

        fields = ('url', 'id', 'label', 'state')

        read_only_fields = (
            'merged_into',
        )


class TerseIdentitySerializer(RelatedField):
    @singledispatch
    def to_representation(self, value):
        return {'id': value.id,
                'label': value.label,
                'qualified_label': value.label,
                'state': value.state}
