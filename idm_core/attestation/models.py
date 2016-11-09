from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from idm_core.person.models import Person

SOURCE_DOCUMENT_TYPE = (
    ('driving-license', 'Driving license'),
    ('passport', 'Passport'),
    ('national-identity-document', 'National identity document'),
    ('bill', 'Bill'),
    ('visa', 'Visa'),
    ('deed-poll', 'Deed poll'),
    ('other', 'Other'),
)


class SourceDocument(models.Model):
    person = models.ForeignKey(Person, related_name='source_documents')
    type = models.CharField(max_length=32, choices=SOURCE_DOCUMENT_TYPE)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='validated_source_documents')
    active = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    label = models.CharField(max_length=256, blank=True)


class SourceDocumentPage(models.Model):
    source_document = models.ForeignKey(SourceDocument)
    page_number = models.PositiveSmallIntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=255)
    image = models.ImageField()


class Attestation(models.Model):
    source_document = models.ForeignKey(SourceDocument)

    attests_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attests_object_id = models.PositiveIntegerField()

    attests = GenericForeignKey('attests_content_type', 'attests_object_id')


class Attestable(DirtyFieldsMixin, models.Model):
    attestations = GenericRelation(Attestation,
                                   content_type_field='attests_content_type',
                                   object_id_field='attests_object_id')

    def save(self, *args, **kwargs):
        if self.is_dirty() and self.attestations.exists():
            raise ValidationError("Can't change an attested {}".format(self._meta.verbose_name))
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
