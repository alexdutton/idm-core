from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from idm_core.attestation.mixins import Attestable


class IdentifierType(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)
    applicable_to = models.ManyToManyField(ContentType)
    applicable_to_all = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('id',)


class Identifier(Attestable, models.Model):
    identity_id = models.UUIDField()
    identity_content_type = models.ForeignKey(ContentType)
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    type = models.ForeignKey(IdentifierType)
    value = models.CharField(max_length=64)

    class Meta:
        unique_together = (('type', 'value'),)
        index_together = (('type', 'identity_content_type', 'identity_id'), ('type', 'value'))
