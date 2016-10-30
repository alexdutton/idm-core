from rest_framework import serializers

from . import models


class ContactSerializer(serializers.ModelSerializer):
    pass


class EmailSerializer(ContactSerializer):
    class Meta:
        model = models.Email


class TelephoneSerializer(ContactSerializer):
    class Meta:
        model = models.Email


class AddressSerializer(ContactSerializer):
    class Meta:
        model = models.Address


class EmbeddedEmailSerializer(EmailSerializer):
    identity = serializers.CharField(required=False, source='identity_id', write_only=True)

    class Meta(EmailSerializer.Meta):
        pass