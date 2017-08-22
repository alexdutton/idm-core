from rest_framework import serializers

from idm_core.application.mixins import ManageableModelSerializer
from idm_core.identifier.serializers import IdentifiableSerializer
from idm_core.identity.serializers import TypeMixin
from . import models


class RelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'label')


class TersePersonSerializer(TypeMixin, IdentifiableSerializer, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:person-detail')
    merged_into = serializers.HyperlinkedRelatedField(queryset=models.Person.objects.all(),
                                                      view_name='api:person-detail')

    class Meta:
        model = models.Person
        fields = ('id', 'url', 'label', 'state', 'merged_into')


class RelationshipSerializer(ManageableModelSerializer, serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(read_only=True)
    suspended = serializers.BooleanField(read_only=True)
    type = RelationshipTypeSerializer(read_only=True)
    organization_id = serializers.UUIDField()
    identity = TersePersonSerializer()
    identity_id = serializers.UUIDField()
    type_id = serializers.CharField()

    class Meta(ManageableModelSerializer.Meta):
        fields = ManageableModelSerializer.Meta.fields + (
            'id', 'identity', 'organization', 'organization_id', 'start_date', 'end_date', 'effective_start_date',
            'effective_end_date', 'review_date', 'suspended_until', 'comment', 'dependent_on', 'state', 'suspended',
            'type', 'type_id', 'identity_id')

