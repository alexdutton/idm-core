from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, ValidationError

from idm_core import models
from idm_core.contact.serializers import EmbeddedEmailSerializer
from idm_core.identifier.serializers import EmbeddedIdentifierSerializer


class TypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = self.Meta.model.__name__
        return data


from idm_core.models import Person
from idm_core.name.serializers import NameSerializer, EmbeddedNameSerializer
from idm_core.nationality.models import Country, Nationality
from idm_core.nationality.serializers import CountrySerializer, NationalitySerializer, EmbeddedNationalitySerializer


class PersonSerializer(TypeMixin, HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedPersonField(view_name='person-detail', lookup_field='uuid')
    id = serializers.UUIDField(read_only=True)
    names = EmbeddedNameSerializer(many=True, default=())
    nationalities = EmbeddedNationalitySerializer(many=True, default=(), source='nationality_set')
    emails = EmbeddedEmailSerializer(many=True, default=())
    identifiers = EmbeddedIdentifierSerializer(many=True, default=())

    class Meta:
        model = Person

        fields = (
            'id', 'sex', 'date_of_birth', 'date_of_death', 'deceased', 'state', 'identifiers',
            'primary_email', 'primary_username', 'names', 'nationalities', 'emails',
        )

        read_only_fields = (
            'merged_into',
        )

    def create(self, validated_data):
        if 'state' in validated_data and validated_data['state'] not in ('new', 'active'):
            raise ValidationError("Can only create identities in states 'new' or 'active'.")
        names = validated_data.pop('names', ())
        emails = validated_data.pop('emails', ())
        nationalities = validated_data.pop('nationality_set', ())
        identifiers = validated_data.pop('identifiers', ())
        person = super(PersonSerializer, self).create(validated_data)
        for name in names:
            name['person'] = person
        for email in emails:
            email['person'] = person
        for nationality in nationalities:
            nationality['person'] = person
        for identifier in identifiers:
            identifier['person'] = person
        self.fields['names'].create(names)
        self.fields['emails'].create(emails)
        self.fields['nationalities'].create(nationalities)
        self.fields['identifiers'].create(identifiers)
        return person
