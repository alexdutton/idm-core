from xml.sax.saxutils import escape

import collections
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete

from idm_core.attestation.models import Attestable
from idm_core.name.fields import JSONSchemaField
from idm_core.person.models import Person

NAME_COMPONENT_TYPE_CHOICES = (
    ('title', 'Title'),
    ('given', 'Given name'),
    ('middle', 'Middle name'),
    ('family', 'Family name'),
    ('suffix', 'Suffix'),
    ('mononym', 'Name'),
)


components_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": [choice[0] for choice in NAME_COMPONENT_TYPE_CHOICES],
            },
            "value": {
                "type": "string",
            },
        },
        "required": ["type", "value"],
        "additionalProperties": False,
    },
}


class NameContext(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.TextField()

    def __str__(self):
        return self.label


class Name(Attestable, models.Model):
    person = models.ForeignKey(Person, related_name='names')

    plain = models.TextField(blank=True)
    plain_full = models.TextField(blank=True)
    marked_up = models.TextField(blank=True)
    familiar = models.TextField(blank=True)
    sort = models.TextField(blank=True)
    first = models.TextField(blank=True)
    last = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    space_delimited = models.BooleanField(default=True)
    components = JSONSchemaField(schema=components_schema)
    contexts = models.ManyToManyField(NameContext)

    def __str__(self):
        return self.plain_full

    def save(self, *args, **kwargs):
        components = self.components
        components_by_type = collections.defaultdict(list)
        for component in components:
            components_by_type[component['type']].append(component['value'])

        delimiter = ' ' if self.space_delimited else ''

        self.plain = delimiter.join(c['value'] for c in components if c['type'] in ('given', 'family', 'mononym'))
        self.plain_full = delimiter.join(c['value'] for c in components)
        self.marked_up = '<name>{}</name>'.format(
            delimiter.join('<{type}>{value}</{type}>'.format(type=c['type'], value=escape(c['value']))
                     for c in components))
        self.familiar = ''
        for component in components:
            if component['type'] == 'given':
                self.familiar = component['value']
                break
        else:
            for component in components:
                if component['type'] == 'mononym':
                    self.familiar = component['value']
                    break

        if 'family' in components_by_type:
            self.sort = delimiter.join(components_by_type['family'])
            if 'given' in components_by_type:
                for component in components:
                    # If a given name precedes a family name, we've reversed their order, so add a ', '.
                    # If the family name comes first, stop looking for a given name.
                    if component['type'] == 'given':
                        self.sort += ', '
                        break
                    elif component['type'] == 'family':
                        break
                self.sort += delimiter.join(components_by_type['given'] + components_by_type['middle'])
        elif 'mononym' in components_by_type:
            if len(components) != 1:
                raise ValidationError("If there's a mononym, there must be only one component")
            self.sort = delimiter.join(components_by_type['mononym'])
        else:
            self.sort = self.plain

        self.first, self.last = '', ''
        for component in components:
            if component['type'] in ('given', 'family'):
                if not self.first and 'given' in components_by_type:
                    self.first = component['value']
                elif not self.last:
                    self.last = component['value']

        super(Name, self).save()


def name_changed(instance, **kwargs):
    person = instance.person
    names = list(person.names.filter(active=True).order_by('id'))
    names_by_context = collections.defaultdict(list)
    for name in names:
        for context in name.contexts.all():
            names_by_context[context.pk].append(name)

    for context in ('presentational', 'legal', 'informal'):
        if context in names_by_context:
            person.primary_name = names_by_context[context][0]
            break
    else:
        person.primary_name = None

    person.save()

post_save.connect(name_changed, sender=Name)
post_delete.connect(name_changed, sender=Name)

