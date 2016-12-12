from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError, ModelSerializer

from idm_core.contact.serializers import EmbeddedEmailSerializer
from idm_core.identifier.serializers import EmbeddedIdentifierSerializer


class TypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = self.Meta.model.__name__
        return data


class IdentityTypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = instance.type_id.title()
        return data


from idm_core.identity import models
from idm_core.name.serializers import EmbeddedNameSerializer
from idm_core.nationality.serializers import EmbeddedNationalitySerializer


class InvertedBooleanField(serializers.BooleanField):
    def to_internal_value(self, data):
        return not super().to_internal_value(data)

    def to_representation(self, value):
        return not super().to_representation(value)


class IdentityTypeSerializer(TypeMixin, ModelSerializer):
    class Meta:
        model = models.IdentityType

        fields = ('id', 'label')


class IdentitySerializer(IdentityTypeMixin, HyperlinkedModelSerializer):
    class Meta:
        model = models.Identity

        fields = ('url', 'id', 'label', 'type_id')

        read_only_fields = (
            'merged_into',
        )


class PlainPersonSerializer(IdentitySerializer):
    url = serializers.HyperlinkedIdentityField(view_name='identity-detail')
    id = serializers.UUIDField(read_only=True)
    date_of_birth = serializers.DateField(source='begin_date', required=False)
    date_of_death = serializers.DateField(source='end_date', required=False)
    deceased = InvertedBooleanField(source='extant', required=False)

    class Meta(IdentitySerializer.Meta):
        fields = IdentitySerializer.Meta.fields + (
            'sex', 'date_of_birth', 'date_of_death', 'deceased', 'state', 'identifiers',
            'primary_email', 'primary_username',
        )


class PersonSerializer(PlainPersonSerializer):
    id = serializers.UUIDField(read_only=True)
    type_id = serializers.ReadOnlyField(default='person')
    names = EmbeddedNameSerializer(many=True, default=())
    nationalities = EmbeddedNationalitySerializer(many=True, default=(), source='nationality_set')
    emails = EmbeddedEmailSerializer(many=True, default=())
    identifiers = EmbeddedIdentifierSerializer(many=True, default=())

    class Meta(PlainPersonSerializer.Meta):
        fields = PlainPersonSerializer.Meta.fields + ('names', 'nationalities', 'emails')

    def create(self, validated_data):
        if 'state' in validated_data and validated_data['state'] not in ('new', 'active'):
            raise ValidationError("Can only create identities in states 'new' or 'active'.")
        names = validated_data.pop('names', ())
        emails = validated_data.pop('emails', ())
        nationalities = validated_data.pop('nationality_set', ())
        identifiers = validated_data.pop('identifiers', ())
        person = super(PersonSerializer, self).create(validated_data)
        for name in names:
            name['identity'] = person
        for email in emails:
            email['identity'] = person
        for nationality in nationalities:
            nationality['identity'] = person
        for identifier in identifiers:
            identifier['identity'] = person
        self.fields['names'].create(names)
        self.fields['emails'].create(emails)
        self.fields['nationalities'].create(nationalities)
        self.fields['identifiers'].create(identifiers)
        return person
