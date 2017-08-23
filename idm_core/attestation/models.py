from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from idm_core.identity.models import Identity


class SourceDocumentType(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class SourceDocument(models.Model):
    identity_content_type = models.ForeignKey(ContentType)
    identity_id = models.UUIDField()
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    type = models.ForeignKey(SourceDocumentType)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='validated_source_documents')
    active = models.BooleanField(default=False)
    label = models.CharField(max_length=256, blank=True)
    document = models.FileField()
    encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class Attestation(models.Model):
    source_document = models.ForeignKey(SourceDocument)

    attests_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attests_object_id = models.PositiveIntegerField()

    attests = GenericForeignKey('attests_content_type', 'attests_object_id')

