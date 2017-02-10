from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db import models

from dirtyfields import DirtyFieldsMixin
from rest_framework.exceptions import ValidationError


class Attestable(DirtyFieldsMixin, models.Model):
    attestations = GenericRelation('attestation.Attestation',
                                   content_type_field='attests_content_type',
                                   object_id_field='attests_object_id')
    attested_by = ArrayField(models.SlugField(), default=[])

    changeable_when_attested = frozenset({'attested_by'})

    def save(self, *args, **kwargs):
        if self.attested_by and set(self.get_dirty_fields()) - self.changeable_when_attested:
            raise ValidationError("Can't change an attested {}".format(self._meta.verbose_name))
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
