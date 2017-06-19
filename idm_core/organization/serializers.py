from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import HyperlinkedModelSerializer

from idm_core.identifier.serializers import EmbeddedIdentifierSerializer
from idm_core.identity.serializers import TypeMixin
from idm_core.relationship.serializers import RelationshipSerializer, RelationshipTypeSerializer

from . import models


class OrganizationSerializer(TypeMixin, HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:organization-detail')
    identifiers = EmbeddedIdentifierSerializer(many=True, default=())

    class Meta:
        model = models.Organization
        fields = ('id', 'label', 'tags', 'identifiers', 'url')

    def create(self, validated_data):
        if 'state' in validated_data and validated_data['state'] not in ('established', 'active'):
            raise ValidationError("Can only create identities in states 'established' or 'active'.")
        identifiers = validated_data.pop('identifiers', ())
        organization = super(OrganizationSerializer, self).create(validated_data)

        for identifier in identifiers:
            identifier['identity'] = organization
        self.fields['identifiers'].create(identifiers)
        return organization


class TerseOrganizationSerializer(OrganizationSerializer):
    pass


class AffiliationTypeSerializer(HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.AffiliationType


class RoleTypeSerializer(HyperlinkedModelSerializer):
    class Meta(RelationshipTypeSerializer.Meta):
        model = models.RoleType


class AffiliationSerializer(RelationshipSerializer):
    type = AffiliationTypeSerializer(read_only=True)
    organization = TerseOrganizationSerializer(read_only=True)

    class Meta(RelationshipSerializer.Meta):
        model = models.Affiliation


class RoleSerializer(RelationshipSerializer):
    type = RoleTypeSerializer(read_only=True)
    organization = TerseOrganizationSerializer(read_only=True)

    class Meta(RelationshipSerializer.Meta):
        model = models.Role
