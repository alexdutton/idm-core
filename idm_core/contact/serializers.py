from rest_framework import serializers

from . import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('context', 'affiliation', 'identity', 'validated')


class EmbeddedContactSerializer(ContactSerializer):
    identity = serializers.Field(required=False, write_only=True)

    class Meta:
        fields = ('identity', 'context')


class EmailSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Email


class TelephoneSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Email


class AddressSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Address


class OnlineAccountSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.OnlineAccount


class EmbeddedEmailSerializer(EmailSerializer, EmbeddedContactSerializer):
    class Meta(EmailSerializer.Meta, EmbeddedContactSerializer.Meta):
        fields = ('value', 'identity', 'context', 'validated')
