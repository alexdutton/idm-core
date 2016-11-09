from rest_framework import serializers

from . import models


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(read_only=True)
    suspended = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ('person', 'organization', 'start_date', 'end_date', 'effective_start_date', 'effective_end_date',
                  'review_date', 'suspended_until', 'comment', 'dependent_on', 'state', 'suspended')
        read_only_fields = ('person', 'organization', 'state', 'suspended')


class AffiliationSerializer(RelationshipSerializer):
    class Meta(RelationshipSerializer.Meta):
        model = models.Affiliation


class RoleSerializer(RelationshipSerializer):
    class Meta(RelationshipSerializer.Meta):
        model = models.Role


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization


class RelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'label')


class AffiliationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.AffiliationType


class RoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.RoleType
