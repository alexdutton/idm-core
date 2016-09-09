from django.db import models

from oxidentity.attestation.models import Attestable
from oxidentity.models import Person


class IdentifierType(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)


class Identifier(Attestable, models.Model):
    type = models.ForeignKey(IdentifierType)
    person = models.ForeignKey(Person, db_index=True)
    value = models.CharField(max_length=64)

    class Meta:
        unique_together = (('type', 'person'), ('type', 'value'))
        index_together = (('type', 'person'), ('type', 'value'))