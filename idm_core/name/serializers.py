import re
from rest_framework import fields, serializers

from idm_core.attestation.serializers import Attestable

from . import models
from .utils import intersperse


class ParseNameField(fields.Field):
    titles = frozenset('mr miss mrs mx ms dr prof professor rh sir lord baron'.split())
    suffixes = frozenset('mp mep am msp jr jnr sr snr obe mbe kbe frs honfrs formemrs fraes esq'.split())

    def get_value(self, dictionary):
        return dictionary.get('parse', fields.empty)

    def to_internal_value(self, data):
        blanks = {'.', '-', None, ''}
        components = []
        if not data:
            pass
        elif isinstance(data, str):
            data = re.findall(r"([\w'.\-]+)|([^\w'.\-]+)", data)
            components = [{'type': None, 'value': c[0]} if c[0] else c[1] for c in data if c[1] or c[0] not in blanks]
            while components and isinstance(components[0], str):
                components.pop(0)
            while components and isinstance(components[-1], str):
                components.pop(-1)
            non_whitespace = [c for c in components if isinstance(c, dict)]

            # Handle titles
            while non_whitespace and non_whitespace[0]['value'].lower() in self.titles:
                non_whitespace[0]['type'] = 'title'
                non_whitespace.pop(0)
            # … and then suffixes
            while non_whitespace and non_whitespace[-1]['value'].lower() in self.suffixes:
                non_whitespace[-1]['type'] = 'suffix'
                non_whitespace.pop(-1)

            # If we only have one component left, it's a mononym
            if len(non_whitespace) == 1:
                non_whitespace[0]['type'] = 'mononym'
            else:
                if non_whitespace:
                    non_whitespace.pop(0)['type'] = 'given'
                if non_whitespace:
                    non_whitespace.pop(-1)['type'] = 'family'
                for component in non_whitespace:
                    component['type'] == 'middle'
        elif isinstance(data, dict):
            for k in list(data):
                if data[k] in blanks:
                    del data[k]
            if 'title' in data:
                components.append({'type': 'title', 'value': data.pop('title')})
            if len(data) == 1:
                components.append({'type': 'mononym', 'value': data.popitem()[1]})
            if len(data) > 1 and 'first' in data:
                components.append({'type': 'given', 'value': data['first']})
            if len(data) > 1 and 'last' in data:
                components.append({'type': 'family', 'value': data['last']})
            components = list(intersperse(components, ' '))

        return components or None


class NameSerializer(Attestable, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:name-detail')
    identity = serializers.HyperlinkedRelatedField(read_only=True, view_name='api:person-detail')
    context = serializers.PrimaryKeyRelatedField(queryset=models.NameContext.objects.all())

    components = fields.JSONField(required=False)
    parse = ParseNameField(source='components', required=False, write_only=True)

    def validate(self, attrs):
        if 'components' not in attrs:
            raise serializers.ValidationError('Either components or parse is required.')
        return attrs

    class Meta:
        model = models.Name

        fields = ('identity', 'plain', 'plain_full', 'marked_up', 'familiar', 'sort', 'first', 'last', 'active',
                  'components', 'parse', 'context', 'attestations', 'url')

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
