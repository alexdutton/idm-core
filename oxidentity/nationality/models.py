from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from oxidentity.attestation.models import Attestation, Attestable
from oxidentity.models import Person


class Country(models.Model):
    label = models.TextField()
    alpha_2 = models.CharField(max_length=2, null=True, unique=True, db_index=True)
    alpha_3 = models.CharField(max_length=3, null=True, unique=True, db_index=True)
    numeric = models.CharField(max_length=3, null=True, unique=True, db_index=True)

    people = models.ManyToManyField(Person, through='nationality.Nationality', related_name='nationalities')

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('label',)


class Nationality(Attestable, models.Model):
    person = models.ForeignKey(Person)
    nationality = models.ForeignKey(Country)
