import uuid
from datetime import timedelta

import django_fsm
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

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
    subject_to_approval = models.BooleanField()
    aspect_ratio = models.FloatField(null=True, blank=True)
    instructions = models.TextField()

    # Generous defaults
    max_width = models.IntegerField(default=3840)
    max_height = models.IntegerField(default=2160)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    identity_id = models.UUIDField()
    identity_content_type = models.ForeignKey(ContentType)
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    context = models.ForeignKey(ImageContext)

    image = models.ImageField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    state = django_fsm.FSMField(choices=IMAGE_STATE_CHOICES, default='proposed')

    @django_fsm.transition(state, source=['proposed', 'rejected'], target='approved')
    def approve(self):
        pass

    def recent_photo(self):
        return now() - self.created < timedelta(3650)

    @django_fsm.transition(state, source=['proposed', 'accepted'], target='rejected',
                           conditions=[recent_photo])
    def reject(self):
        for image in self.objects.filter(identity_id=self.identity_id,
                                         context=self.context,
                                         state='accepted').select_for_update():
            image.retire()

    @django_fsm.transition(state, source='*', target='previous')
    def retire(self):
        pass

    def save(self, *args, **kwargs):
        # Automatic approval for images that don't need approving
        if self.state == 'proposed' and not self.context.subject_to_approval:
            self.approve()
        return super().save(*args, **kwargs)

    def get_image_url(self):
        return reverse('image:image-file', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('image:image-detail', args=(self.pk,))