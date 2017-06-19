from rest_framework import serializers

from idm_core.application.mixins import ManageableModelSerializer
from idm_core.identity.serializers import IdentityRelatedField
from . import models


class ContactSerializer(ManageableModelSerializer, serializers.ModelSerializer):
    identity = IdentityRelatedField()

    class Meta:
        fields = ('url', 'context', 'affiliation', 'identity', 'validated') + ManageableModelSerializer.Meta.fields


class EmbeddedContactSerializer(ContactSerializer):
    identity = serializers.Field(required=False, write_only=True)

    class Meta:
        fields = ('identity', 'context')


class EmailSerializer(ContactSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:email-detail')
    class Meta(ContactSerializer.Meta):
        model = models.Email


class TelephoneSerializer(ContactSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:telephone-detail')
    class Meta(ContactSerializer.Meta):
        model = models.Email


class AddressSerializer(ContactSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:address-detail')
    class Meta(ContactSerializer.Meta):
        model = models.Address


class OnlineAccountSerializer(ContactSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:online-account-detail')
    provider_id = serializers.CharField()

    class Meta(ContactSerializer.Meta):
        model = models.OnlineAccount
        fields = ('provider_id', 'screen_name') + ContactSerializer.Meta.fields


class EmbeddedEmailSerializer(EmailSerializer, EmbeddedContactSerializer):
    class Meta(EmailSerializer.Meta, EmbeddedContactSerializer.Meta):
        fields = ('value', 'identity', 'context', 'validated')
