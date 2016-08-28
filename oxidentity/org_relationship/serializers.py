from rest_framework import serializers

from . import models


class AffiliationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Affiliation


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Role


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Unit


class AffiliationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AffiliationType


class RoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RoleType

