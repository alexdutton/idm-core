from django.contrib.contenttypes.models import ContentType
from django.db import models

from idm_core.identity.models import IdentityBase


class Application(IdentityBase):
    manageable_content_types = models.ManyToManyField(ContentType)

    def __str__(self):
        return self.label
