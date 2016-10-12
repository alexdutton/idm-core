from rest_framework import serializers

from . import models


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(read_only=True)
    suspended = serializers.BooleanField(read_only=True)


class AffiliationSerializer(RelationshipSerializer):
    class Meta:
        model = models.Affiliation


class RoleSerializer(RelationshipSerializer):
    class Meta:
        model = models.Role


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization


class AffiliationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AffiliationType


class RoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RoleType

