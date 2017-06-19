from rest_framework import serializers

from idm_core.application.mixins import ManageableModelSerializer
from idm_core.person.serializers import PersonSerializer, TersePersonSerializer
from . import models


class RelationshipTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'label')


class RelationshipSerializer(ManageableModelSerializer, serializers.HyperlinkedModelSerializer):
    state = serializers.CharField(read_only=True)
    suspended = serializers.BooleanField(read_only=True)
    identity = TersePersonSerializer(read_only=True)
    type = RelationshipTypeSerializer(read_only=True)
    organization_id = serializers.UUIDField()
    identity_id = serializers.UUIDField()
    type_id = serializers.CharField()

    class Meta(ManageableModelSerializer.Meta):
        fields = ManageableModelSerializer.Meta.fields + (
            'id', 'identity', 'organization', 'organization_id', 'start_date', 'end_date', 'effective_start_date',
            'effective_end_date', 'review_date', 'suspended_until', 'comment', 'dependent_on', 'state', 'suspended',
            'type', 'type_id', 'identity_id')

