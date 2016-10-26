from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from idm_identity.contact.serializers import EmbeddedEmailSerializer


class TypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = self.Meta.model.__name__
        return data


from idm_identity.gender.serializers import GenderSerializer, PronounField
from idm_identity.models import Identity
from idm_identity.name.serializers import NameSerializer, EmbeddedNameSerializer
from idm_identity.nationality.models import Country, Nationality
from idm_identity.nationality.serializers import CountrySerializer, NationalitySerializer, EmbeddedNationalitySerializer


class IdentitySerializer(TypeMixin, HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='identity-detail', lookup_field='uuid')
    id = serializers.UUIDField(read_only=True)
    names = EmbeddedNameSerializer(many=True, default=())
    # gender = GenderSerializer(read_only=True)
    # legal_gender = GenderSerializer(read_only=True)
    # gender_id = serializers.CharField(allow_null=True, default=None)
    # legal_gender_id = serializers.CharField(allow_null=True, default=None)
    pronouns = PronounField(default={})
    nationalities = EmbeddedNationalitySerializer(many=True, default=(), source='nationality_set')
    emails = EmbeddedEmailSerializer(many=True, default=())

    class Meta:
        model = Identity

        read_only_fields = (
            'merged_into',
        )

    def create(self, validated_data):
        names = validated_data.pop('names', ())
        emails = validated_data.pop('emails', ())
        nationalities = validated_data.pop('nationality_set', ())
        identity = super(IdentitySerializer, self).create(validated_data)
        for name in names:
            name['identity'] = identity
        for email in emails:
            email['identity'] = identity
        for nationality in nationalities:
            nationality['identity'] = identity
        self.fields['names'].create(names)
        self.fields['emails'].create(emails)
        self.fields['nationalities'].create(nationalities)
        return identity