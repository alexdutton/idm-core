from xml.sax.saxutils import escape

import collections
from dirtyfields import DirtyFieldsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from rest_framework.reverse import reverse

from idm_core.acceptance.models import AcceptableModel
from idm_core.attestation.mixins import Attestable
from idm_core.name.fields import JSONSchemaField
from idm_core.identity.models import Identity
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
        "oneOf": [{
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
        }, {
            "type": "string",
        }],
    },
}


class NameContext(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.TextField()
    subject_to_acceptance = models.BooleanField(default=True)
    only_one_accepted = models.BooleanField(default=True)

    def __str__(self):
        return self.label


class Name(Attestable, DirtyFieldsMixin, AcceptableModel):
    identity = models.ForeignKey(Person, related_name='names')

    plain = models.TextField(blank=True)
    plain_full = models.TextField(blank=True)
    marked_up = models.TextField(blank=True)
    familiar = models.TextField(blank=True)
    sort = models.TextField(blank=True)
    first = models.TextField(blank=True)
    last = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    components = JSONSchemaField(schema=components_schema)
    context = models.ForeignKey(NameContext)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plain_full

    def get_absolute_url(self):
        return reverse('name:name-detail', args=[self.pk])

    @property
    def subject_to_acceptance(self):
        return self.context.subject_to_acceptance

    @property
    def only_one_accepted(self):
        return self.context.only_one_accepted

    def get_acceptance_queryset(self):
        return type(self).objects.filter(identity_id=self.identity_id, context_id=self.context_id)

    def save(self, *args, **kwargs):
        components = self.components
        components_by_type = collections.defaultdict(list)
        components_with_whitespace = []
        for component in components:
            if isinstance(component, dict):
                components_by_type[component['type']].append(component['value'])
                components_with_whitespace.append(component)
            else:
                components_with_whitespace.append({'type': 'whitespace', 'value': component})

        # This strips out e.g. titles, suffixes and middle names, and then removes leading and trailing whitespace.
        # Embedded whitespace is then pared down.
        plain = [c for c in components_with_whitespace
                 if c['type'] in ('whitespace', 'family', 'given', 'mononym')]
        while plain and plain[0]['type'] == 'whitespace':
            plain.pop(0)
        while plain and plain[-1]['type'] == 'whitespace':
            plain.pop(-1)
        i = 0
        while i < len(plain) - 1:
            if plain[i]['type'] == 'whitespace' and plain[i+1]['type'] == 'whitespace':
                plain[i]['value'] += plain[i+1]['value'].strip()
                del plain[i+1]
            else:
                i += 1
        self.plain = ''.join(c['value'] for c in plain)

        self.plain_full = ''.join(c['value'] for c in components_with_whitespace)
        self.marked_up = '<name>{}</name>'.format(
            ''.join('<{type}>{value}</{type}>'.format(type=c['type'], value=escape(c['value'])) if isinstance(c, dict) else c
                     for c in components))
        self.familiar = ''
        for component in components_with_whitespace:
            if component['type'] == 'given':
                self.familiar = component['value']
                break
        else:
            for component in components_with_whitespace:
                if component['type'] == 'mononym':
                    self.familiar = component['value']
                    break

        if 'family' in components_by_type:
            self.sort = ' '.join(components_by_type['family'])
            if 'given' in components_by_type:
                for component in components_with_whitespace:
                    # If a given name precedes a family name, we've reversed their order, so add a ', '.
                    # If the family name comes first, stop looking for a given name.
                    if component['type'] == 'given':
                        self.sort += ', '
                        break
                    elif component['type'] == 'family':
                        break
                self.sort += ' '.join(components_by_type['given'] + components_by_type['middle'])
        elif 'mononym' in components_by_type:
            if len(components) != 1:
                raise ValidationError("If there's a mononym, there must be only one component")
            self.sort = ' '.join(components_by_type['mononym'])
        else:
            self.sort = self.plain

        self.first, self.last = '', ''
        for component in components_with_whitespace:
            if component['type'] in ('given', 'family'):
                if not self.first and 'given' in components_by_type:
                    self.first = component['value']
                elif not self.last:
                    self.last = component['value']
            elif component['type'] == 'mononym':
                self.last = component['value']
                break

        super(Name, self).save()


def name_changed(instance: Name, **kwargs):
    identity = instance.identity
    names = list(identity.names.filter(active=True).order_by('id'))
    names_by_context = collections.defaultdict(list)
    for name in names:
        names_by_context[name.context_id].append(name)

    for context in ('presentational', 'legal', 'informal'):
        if context in names_by_context:
            identity.primary_name = names_by_context[context][0]
            break
    else:
        identity.primary_name = None

    identity.save()


def update_primary_name_if_identity_changed(instance: Name, **kwargs):
    if 'identity' in instance.get_dirty_fields(check_relationship=True):
        try:
            person = instance.primary_name_of
        except Name.primary_name_of.RelatedObjectDoesNotExist:
            pass
        else:
            person.primary_name = None
            person.save()


pre_save.connect(update_primary_name_if_identity_changed, sender=Name)

post_save.connect(name_changed, sender=Name)
post_delete.connect(name_changed, sender=Name)

