from rest_framework import serializers

from .models import Gender


class PronounField(serializers.Field):
    pronoun_types = ('subject', 'object', 'possessiveDeterminer', 'possessivePronoun', 'reflexive')

    def to_representation(self, value):
        if isinstance(value, dict):
            return value
        return dict(zip(self.pronoun_types, value.split()))

    def to_internal_value(self, data):
        value = []
        for pronoun_type in self.pronoun_types:
            if pronoun_type in data:
                value.append(data[pronoun_type].strip())
            else:
                break
        return ' '.join(value)

class GenderSerializer(serializers.HyperlinkedModelSerializer):
    pronouns = PronounField()

    class Meta:
        model = Gender
