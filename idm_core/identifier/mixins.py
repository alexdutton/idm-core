from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Identifiable(models.Model):
    identifiers = GenericRelation('identifier.Identifier', 'identity_id', 'identity_content_type')

    class Meta:
        abstract = True