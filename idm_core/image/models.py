import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from idm_core.acceptance.models import AcceptableModel
from idm_core.attestation.mixins import Attestable

IMAGE_STATE_CHOICES = (
    ('proposed', 'proposed'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('previous', 'previous'),
)


class ImageContext(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    label = models.CharField(max_length=255)
    subject_to_acceptance = models.BooleanField()
    min_aspect_ratio_x = models.IntegerField(null=True, blank=True)
    min_aspect_ratio_y = models.IntegerField(null=True, blank=True)
    max_aspect_ratio_x = models.IntegerField(null=True, blank=True)
    max_aspect_ratio_y = models.IntegerField(null=True, blank=True)
    prefer_jpeg = models.BooleanField(default=True)
    instructions = models.TextField()

    # Generous defaults
    max_width = models.IntegerField(default=3840)
    max_height = models.IntegerField(default=2160)


class Image(AcceptableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    identity_id = models.UUIDField()
    identity_content_type = models.ForeignKey(ContentType)
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    context = models.ForeignKey(ImageContext)

    image = models.ImageField(upload_to='image/%Y/%m/%d/')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def subject_to_acceptance(self):
        return self.context.subject_to_acceptance

    def get_acceptance_queryset(self):
        return type(self).objects.filter(identity_id=self.identity_id, context_id=self.context_id)

    def get_image_url(self):
        return reverse('image:image-file', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('image:image-detail', args=(self.pk,))
