from django.db import models

from idm_identity.attestation.models import Attestable
from idm_identity.models import Identity


class IdentifierType(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)


class Identifier(Attestable, models.Model):
    type = models.ForeignKey(IdentifierType)
    identity = models.ForeignKey(Identity, db_index=True)
    value = models.CharField(max_length=64)

    class Meta:
        unique_together = (('type', 'identity'), ('type', 'value'))
        index_together = (('type', 'identity'), ('type', 'value'))