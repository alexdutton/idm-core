from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer


class TypeMixin(object):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@type'] = self.Meta.model.__name__
        return data


from oxidentity.gender.serializers import GenderSerializer, PronounField
from oxidentity.models import Identity
from oxidentity.name.serializers import NameSerializer, EmbeddedNameSerializer
from oxidentity.nationality.models import Country, Nationality
from oxidentity.nationality.serializers import CountrySerializer, NationalitySerializer, EmbeddedNationalitySerializer


class IdentitySerializer(TypeMixin, HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='identity-detail', lookup_field='uuid')
    names = EmbeddedNameSerializer(many=True, default=())
    # gender = GenderSerializer(read_only=True)
    # legal_gender = GenderSerializer(read_only=True)
    # gender_id = serializers.CharField(allow_null=True, default=None)
    # legal_gender_id = serializers.CharField(allow_null=True, default=None)
    pronouns = PronounField(default={})
    nationalities = EmbeddedNationalitySerializer(many=True, default=(), source='nationality_set')

    class Meta:
        model = Identity

        read_only_fields = (
            'merged_into',
        )

    def create(self, validated_data):
        names = validated_data.pop('names', ())
        nationalities = validated_data.pop('nationality_set', ())
        identity = super(IdentitySerializer, self).create(validated_data)
        for name in names:
            name['identity'] = identity
        for nationality in nationalities:
            nationality['identity'] = identity
        self.fields['names'].create(names)
        self.fields['nationalities'].create(nationalities)
        return identity