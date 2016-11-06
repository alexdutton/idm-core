from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from idm_core.attestation.models import Attestation, Attestable
from idm_core.models import Person


class Country(models.Model):
    label = models.TextField()
    alpha_2 = models.CharField(max_length=2, null=True, unique=True, db_index=True)
    alpha_3 = models.CharField(max_length=3, null=True, unique=True, db_index=True)
    numeric = models.CharField(max_length=3, null=True, unique=True, db_index=True)

    identities = models.ManyToManyField(Person, through='nationality.Nationality', related_name='nationalities')

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('label',)


class Nationality(Attestable, models.Model):
    person = models.ForeignKey(Person)
    country = models.ForeignKey(Country)
