from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from idm_core.application.mixins import ManageableModelSerializer
from idm_core.contact.serializers import EmbeddedEmailSerializer
from idm_core.identifier.serializers import EmbeddedIdentifierSerializer, IdentifiableSerializer
from idm_core.identity.serializers import InvertedBooleanField, TypeMixin
from idm_core.name.serializers import EmbeddedNameSerializer, NameSerializer
from idm_core.nationality.serializers import EmbeddedNationalitySerializer

from . import models


class TersePersonSerializer(TypeMixin, IdentifiableSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('id', 'url', 'label', 'state')


class PlainPersonSerializer(ManageableModelSerializer, TersePersonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')
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

        identity_content_type_id, identity_id = ContentType.objects.get_for_model(type(person)).id, person.id

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
