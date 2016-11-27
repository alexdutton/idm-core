from rest_framework import serializers

from idm_core.organization.serializers import TerseOrganizationSerializer
from . import models


class RelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'label')


class AffiliationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.AffiliationType


class RoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.RoleType


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(read_only=True)
    suspended = serializers.BooleanField(read_only=True)
    organization = TerseOrganizationSerializer(read_only=True)

    class Meta:
        fields = ('person', 'organization', 'organization_id', 'start_date', 'end_date', 'effective_start_date', 'effective_end_date',
                  'review_date', 'suspended_until', 'comment', 'dependent_on', 'state', 'suspended', 'type', 'type_id')
        read_only_fields = ('person', 'organization', 'state', 'suspended')


class AffiliationSerializer(RelationshipSerializer):
    type = AffiliationTypeSerializer(read_only=True)

    class Meta(RelationshipSerializer.Meta):
        model = models.Affiliation


class RoleSerializer(RelationshipSerializer):
    type = RoleTypeSerializer(read_only=True)

    class Meta(RelationshipSerializer.Meta):
        model = models.Role
