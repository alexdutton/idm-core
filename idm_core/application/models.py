from django.contrib.contenttypes.models import ContentType
from django.db import models

from idm_core.identity.models import IdentityBase


class Application(IdentityBase):
    manageable_content_types = models.ManyToManyField(ContentType,
                                                      through='application.ApplicationMayManageContentType')


class ApplicationMayManageContentType(models.Model):
    application = models.ForeignKey(Application)
    content_type = models.ForeignKey(ContentType)
