from django.db import models

from idm_core.attestation.models import Attestable
from idm_core.identity.models import Identity, IdentityType


class IdentifierType(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)
    applicable_to = models.ManyToManyField(IdentityType)


class Identifier(Attestable, models.Model):
    type = models.ForeignKey(IdentifierType)
    identity = models.ForeignKey(Identity, db_index=True, related_name='identifiers')
    value = models.CharField(max_length=64)

    class Meta:
        unique_together = (('type', 'value'),)
        index_together = (('type', 'identity'), ('type', 'value'))
