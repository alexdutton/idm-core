from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from oxidentity.gender.models import Gender
from oxidentity.gender.serializers import GenderSerializer, PronounField
from oxidentity.models import Person
from oxidentity.name.serializers import NameSerializer, EmbeddedNameSerializer
from oxidentity.nationality.models import Country, Nationality
from oxidentity.nationality.serializers import CountrySerializer


class PersonSerializer(HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='person-detail', lookup_field='uuid')
    names = EmbeddedNameSerializer(many=True, default=())
    # gender = GenderSerializer(read_only=True)
    # legal_gender = GenderSerializer(read_only=True)
    # gender_id = serializers.CharField(allow_null=True, default=None)
    # legal_gender_id = serializers.CharField(allow_null=True, default=None)
    pronouns = PronounField(default={})
    nationalities = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='country-detail')

    class Meta:
        model = Person

        read_only_fields = (
            'merged_into',
        )

    def create(self, validated_data):
        names = validated_data.pop('names', ())
        person = super(PersonSerializer, self).create(validated_data)
        for name in names:
            name['person'] = person
        self.fields['names'].create(names)
        return person