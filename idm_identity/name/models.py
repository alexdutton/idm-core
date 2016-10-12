import collections
from xml.sax.saxutils import escape

from django.db import models
from django.db.models.signals import post_save, post_delete

from idm_identity.attestation.models import Attestable
from idm_identity.models import Identity

NAME_COMPONENT_TYPE_CHOICES = (
    ('title', 'Title'),
    ('given', 'Given name'),
    ('middle', 'Middle name'),
    ('family', 'Family name'),
    ('suffix', 'Suffix'),
    ('name', 'Name'),
)


class NameContext(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.TextField()

    def __str__(self):
        return self.label


class Name(Attestable, models.Model):
    identity = models.ForeignKey(Identity, related_name='names')

    plain = models.TextField(blank=True)
    plain_full = models.TextField(blank=True)
    marked_up = models.TextField(blank=True)
    familiar = models.TextField(blank=True)
    sort = models.TextField(blank=True)
    first = models.TextField(blank=True)
    last = models.TextField(blank=True)

    active = models.BooleanField(default=True)
    contexts = models.ManyToManyField(NameContext)

    def __str__(self):
        return self.plain_full

    def save(self, *args, **kwargs):
        components = list(self.components.all())
        components_by_type = collections.defaultdict(list)
        for component in components:
            components_by_type[component.type].append(component.value)

        self.plain = ' '.join(c.value for c in components if c.type in ('given', 'family', 'name'))
        self.plain_full = ' '.join(c.value for c in components)
        self.marked_up = '<name>{}</name>'.format(
            ' '.join('<{type}>{value}</{type}>'.format(type=c.type, value=escape(c.value))
                     for c in components))
        self.familiar = ''
        for component in components:
            if component.type == 'given':
                self.familiar = component.value
                break
        else:
            for component in components:
                if component.type == 'name':
                    self.familiar = component.value
                    break

        if 'family' in components_by_type:
            self.sort = ' '.join(components_by_type['family'])
            if 'given' in components_by_type:
                self.sort += ', ' + ' '.join(components_by_type['given'])
        elif 'name' in components_by_type:
            self.sort = ' '.join(components_by_type['name'])
        else:
            self.sort = self.plain

        self.first, self.last = '', ''
        for component in components:
            if component.type in ('given', 'family'):
                if not self.first and 'given' in components_by_type:
                    self.first = component.value
                elif not self.last:
                    self.last = component.value

        super(Name, self).save()


class NameComponent(models.Model):
    name = models.ForeignKey(Name, related_name='components')
    order = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=20, choices=NAME_COMPONENT_TYPE_CHOICES)
    value = models.TextField()

    class Meta:
        ordering = ('order',)


def name_component_changed(instance, **kwargs):
    instance.name.save()

post_save.connect(name_component_changed, sender=NameComponent)
post_delete.connect(name_component_changed, sender=NameComponent)


def name_changed(instance, **kwargs):
    identity = instance.identity
    names = list(identity.names.filter(active=True).order_by('id'))
    names_by_context = collections.defaultdict(list)
    for name in names:
        for context in name.contexts.all():
            names_by_context[context.pk].append(name)

    for context in ('presentational', 'formal', 'informal'):
        if context in names_by_context:
            identity.primary_name = names_by_context[context][0]
            break
    else:
        identity.primary_name = None

    identity.save()

post_save.connect(name_changed, sender=Name)
post_delete.connect(name_changed, sender=Name)

