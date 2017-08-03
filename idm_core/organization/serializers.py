from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import HyperlinkedModelSerializer, PrimaryKeyRelatedField

from idm_core.course.models import Course
from idm_core.course.serializers import TerseCourseSerializer
from idm_core.identifier.serializers import EmbeddedIdentifierSerializer
from idm_core.identity.serializers import TypeMixin
from idm_core.relationship.serializers import RelationshipSerializer, RelationshipTypeSerializer

from . import models


class OrganizationSerializer(TypeMixin, HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:organization-detail')
    identifiers = EmbeddedIdentifierSerializer(many=True, default=())
    tags = PrimaryKeyRelatedField(queryset=models.OrganizationTag.objects.all(), many=True)

    class Meta:
        model = models.Organization
        fields = ('id', 'label', 'short_label', 'tags', 'identifiers', 'url')

    def create(self, validated_data):
        if 'state' in validated_data and validated_data['state'] not in ('established', 'active'):
            raise ValidationError("Can only create identities in states 'established' or 'active'.")
        identifiers = validated_data.pop('identifiers', ())
        organization = super(OrganizationSerializer, self).create(validated_data)

        for identifier in identifiers:
            identifier['identity'] = organization
        self.fields['identifiers'].create(identifiers)
        return organization

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        identifiers = validated_data.pop('identifiers', None)
        print(validated_data)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags = tags
        return instance


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
    course = TerseCourseSerializer(read_only=True)
    course_id = PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta(RelationshipSerializer.Meta):
        model = models.Affiliation
        fields = RelationshipSerializer.Meta.fields + ('course', 'course_id')


class EmbeddedAffiliationSerializer(AffiliationSerializer):
    class Meta(AffiliationSerializer.Meta):
        fields = list(AffiliationSerializer.Meta.fields)
        fields.remove('identity')
        fields.remove('identity_id')


class RoleSerializer(RelationshipSerializer):
    type = RoleTypeSerializer(read_only=True)
    organization = TerseOrganizationSerializer(read_only=True)

    class Meta(RelationshipSerializer.Meta):
        model = models.Role
