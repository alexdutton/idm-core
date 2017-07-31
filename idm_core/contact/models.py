from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max
from phonenumber_field.modelfields import PhoneNumberField

from idm_core.application.mixins import ManageableModel
from idm_core.attestation.mixins import Attestable
from idm_core.organization.models import Affiliation
from idm_core.identity.models import Identity


class ContactContext(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=255)


class Contact(Attestable, ManageableModel, models.Model):
    identity_content_type = models.ForeignKey(ContentType)
    identity_id = models.UUIDField()
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    validated = models.BooleanField(default=False)
    affiliation = models.ForeignKey(Affiliation, null=True, blank=True)
    context = models.ForeignKey(ContactContext)
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        unique_together = (('identity_content_type', 'identity_id', 'order'),)
        ordering = ('identity_content_type', 'identity_id', 'order')

    def save(self, *args, **kwargs):
        from .mixins import Contactable
        assert isinstance(self.identity, Contactable)

        if not self.order:
            c = type(self).objects.filter(identity_content_type=self.identity_content_type,
                                          identity_id=self.identity_id).aggregate(Max('order')).get('order__max')
            self.order = 0 if c is None else c + 1
        return super().save(*args, **kwargs)


class Email(Contact):
    value = models.EmailField()

    class Meta:
        verbose_name = 'email address'
        verbose_name_plural = 'email addresses'


# Values taken from RFC 6350
# https://tools.ietf.org/html/rfc6350#section-6.4.1
class TelephoneType(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    label = models.TextField()


class Telephone(Contact):
    type = models.ForeignKey(TelephoneType)
    external = PhoneNumberField()
    internal = models.CharField(max_length=16, blank=True)

    class Meta:
        verbose_name = 'telephone number'


class Address(Contact):
    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'


class OnlineAccountProvider(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.TextField()

    def __str__(self):
        return self.label


class OnlineAccount(Contact):
    provider = models.ForeignKey(OnlineAccountProvider)
    screen_name = models.TextField()

    def __str__(self):
        return '{} at {}'.format(self.screen_name, self.provider)