from rest_framework import serializers

from . import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('order',)


class EmailSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Email


class TelephoneSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Email


class AddressSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        model = models.Address


class EmbeddedEmailSerializer(EmailSerializer):
    person = serializers.CharField(required=False, source='person_id', write_only=True)

    class Meta(EmailSerializer.Meta):
        pass
