from rest_framework import fields, serializers

from idm_core.attestation.serializers import Attestable
from idm_core.name.models import NameContext
from . import models


class ParseNameField(fields.Field):
    titles = frozenset('mr miss mrs mx dr prof professor')

    def get_value(self, dictionary):
        return dictionary.get('parse', fields.empty)

    def to_internal_value(self, data):
        blanks = {'.', '-', None, ''}
        components = []
        if not data:
            pass
        elif isinstance(data, str):
            data = [d for d in data.split() if d not in blanks]
            if data[0].lower() in self.titles:
                components.append({'type': 'title', 'value': data.pop(0)})
            if len(data) == 1:
                components.append({'type': 'mononym', 'value': data[0]})
            else:
                components.append({'type': 'given', 'value': data[0]})
                components.extend([{'type': 'middle', 'value': d} for d in data[1:-1]])
                components.append({'type': 'family', 'value': data[-1]})
        elif isinstance(data, dict):
            for k in list(data):
                if data[k] in blanks:
                    del data[k]
            if len(data) is 1:
                components.append({'type': 'mononym', 'value': data.popitem()[1]})

        return components or None


class NameSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    contexts = serializers.PrimaryKeyRelatedField(queryset=NameContext.objects.all(), many=True)

    components = fields.JSONField(required=False)
    parse = ParseNameField(source='components', required=False, write_only=True)

    def validate(self, attrs):
        if 'components' not in attrs:
            raise serializers.ValidationError('Either components or parse is required.')
        return attrs

    class Meta:
        model = models.Name

        fields = ('identity', 'plain', 'plain_full', 'marked_up', 'familiar', 'sort', 'first', 'last', 'active',
                  'space_delimited', 'components', 'parse', 'contexts', 'attestations')

        read_only_fields = (
            'identity',
            'plain',
            'plain_full'
            'marked_up',
            'familiar',
            'sort',
            'first',
            'last'
        )


class EmbeddedNameSerializer(NameSerializer):
    identity = serializers.CharField(required=False, source='person_id', write_only=True)

    class Meta(NameSerializer.Meta):
        fields = tuple(set(NameSerializer.Meta.fields) - {'attestations'})
