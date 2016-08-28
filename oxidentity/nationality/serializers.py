from rest_framework import serializers

from oxidentity.attestation.serializers import Attestable, AttestationSerializer
from . import models


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Country
        exclude = ('people',)


class NationalitySerializer(Attestable, serializers.ModelSerializer):
    nationality = CountrySerializer()
    class Meta:
        model = models.Nationality
        exclude = ('person',)