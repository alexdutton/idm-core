from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from idm_core.application.mixins import ManageableModelSerializer
from idm_core.contact.serializers import EmbeddedEmailSerializer
from idm_core.identifier.serializers import EmbeddedIdentifierSerializer, IdentifiableSerializer
from idm_core.identity.serializers import TypeMixin, related_identity_to_representation
from idm_core.image.serializers import EmbeddedImageSerializer
from idm_core.name.serializers import EmbeddedNameSerializer, NameSerializer
from idm_core.nationality.serializers import EmbeddedNationalitySerializer
from idm_core.organization.serializers import EmbeddedAffiliationSerializer

from . import models


class TersePersonSerializer(TypeMixin, IdentifiableSerializer, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:person-detail')
    merged_into = serializers.HyperlinkedRelatedField(queryset=models.Person.objects.all(),
                                                      view_name='api:person-detail')

    class Meta:
        model = models.Person
        fields = ('id', 'url', 'label', 'state', 'merged_into')


class PlainPersonSerializer(ManageableModelSerializer, TersePersonSerializer):
    primary_name = NameSerializer()

    class Meta(TersePersonSerializer.Meta):
        model = models.Person
        fields = TersePersonSerializer.Meta.fields + (
            'sex', 'date_of_birth', 'date_of_death', 'deceased', 'identifiers',
            'primary_email', 'primary_username', 'primary_name'
        )


class PersonSerializer(PlainPersonSerializer):
    names = EmbeddedNameSerializer(many=True, default=())
    nationalities = EmbeddedNationalitySerializer(many=True, default=(), source='nationality_set')
    emails = EmbeddedEmailSerializer(many=True, default=())
    identifiers = EmbeddedIdentifierSerializer(many=True, default=())
    affiliations = EmbeddedAffiliationSerializer(many=True, default=(), source='affiliation_set', read_only=True)
    images = EmbeddedImageSerializer(many=True, read_only=True)

    class Meta(PlainPersonSerializer.Meta):
        fields = PlainPersonSerializer.Meta.fields + ('names', 'nationalities', 'emails', 'affiliations', 'images')

    def create(self, validated_data):
        if 'state' in validated_data and validated_data['state'] not in ('established', 'active'):
            raise ValidationError("Can only create identities in states 'established' or 'active'.")
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


@related_identity_to_representation.register(models.Person)
def related_person_to_representation(person, context):
    return PersonSerializer(context=context).to_representation(person)
