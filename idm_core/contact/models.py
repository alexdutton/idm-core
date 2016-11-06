from django.db import models
from django.db.models import Max

from idm_core.org_relationship.models import Affiliation
from idm_core.person.models import Person


class ContactContext(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=255)


class Contact(models.Model):
    person = models.ForeignKey(Person, db_index=True)
    validated = models.BooleanField(default=False)
    affiliation = models.ForeignKey(Affiliation, null=True, blank=True)
    context = models.ForeignKey(ContactContext)
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        unique_together = (('person', 'order'),)
        ordering = ('person', 'order')

    def save(self, *args, **kwargs):
        if not self.order:
            c = type(self).objects.filter(person=self.person).aggregate(Max('order')).get('order__max')
            self.order = 0 if c is None else c + 1
        return super().save(*args, **kwargs)


class Email(Contact):
    person = models.ForeignKey(Person, db_index=True, related_name='emails')
    value = models.EmailField()


class Telephone(Contact):
    value = models.EmailField()


class Address(Contact):
    pass
