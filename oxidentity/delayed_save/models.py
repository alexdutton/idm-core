import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from oxidentity.delayed_save.tasks import save_object


class DelayedSave(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    when = models.DateTimeField()

    @property
    def task_id(self):
        return 'delayed-save.{}.{}'.format(self.content_type_id,
                                           self.object_id)

    def save(self, *args, **kwargs):
        threshold = timezone.now() + datetime.timedelta(seconds=120)
        if self.when < threshold:
            self.schedule()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def schedule(self):
        save_object.apply_async((self.content_type_id, self.object_id),
                                task_id=self.task_id)
