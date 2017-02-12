import uuid

from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_fsm import FSMField, transition
import templated_email


# ISO/IEC 24760-1:2011
from idm_core.contact.mixins import Contactable
from idm_core.identifier.mixins import Identifiable

STATE_CHOICES = (
    ('established', 'established'),
    ('active', 'active'),
    ('archived', 'archived'),
    ('suspended', 'suspended'),
    ('merged', 'merged'), # Not in standard, but used for operational purposes
)

def get_uuid():
    return uuid.uuid4()


class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    identity = models.ForeignKey('identity.Identity', null=True, blank=True)


class Identity(models.Model):
    id = models.UUIDField(primary_key=True)
    content_type = models.ForeignKey(ContentType)

    identity = GenericForeignKey('content_type', 'id')


class IdentityBase(DirtyFieldsMixin, Contactable, Identifiable, models.Model):
    """An identity is the information used to represent an entity in an ICT system.

    The purpose of the ICT system determines which of the attributes describing an entity are used for an identity.
    Within an ICT system an identity shall be the set of those attributes related to an entity which are relevant to
    the particular domain of application served by the ICT system. Depending on the specific requirements of this
    domain, this set of attributes related to the entity (the identity) may, but does not have to be, uniquely
    distinguishable from other identities in the ICT system. (taken from ISO/IEC 24760-1:2011)
    """
    id = models.UUIDField(primary_key=True, editable=False, default=get_uuid)
    label = models.CharField(max_length=1024, blank=True)
    qualified_label = models.CharField(max_length=1024, blank=True)
    sort_label = models.CharField(max_length=1024, blank=True)

    primary_username = models.CharField(blank=True, max_length=32)

    state = FSMField(choices=STATE_CHOICES, default='established')
    merged_into = models.ForeignKey('self', null=True, blank=True, related_name='merged_from')


    @transition(field=state, source='established', target='established',
                conditions=[lambda self: self.emails.exists()])
    def ready_for_activation(self, email=None):
        if not email:
            email = self.emails.order_by('order').first().value
        self.claim_code = get_uuid()
        templated_email.send_templated_mail(template_name='claim-identity',
                                            from_email=settings.DEFAULT_FROM_EMAIL,
                                            to_email=email,
                                            context={'identity': self,
                                                     'claim_url': settings.CLAIM_URL.format(self.claim_code)})

    @transition(field=state, source='established', target='active')
    def activate(self):
        pass

    @transition(field=state, source='active', target='archived')
    def archive(self):
        pass

    @transition(field=state, source='archived', target='established')
    def restore(self):
        pass

    @transition(field=state, source=['established', 'active'], target='merged')
    def merge_into(self, other):
        self.merged_into = other

    @transition(field=state, source='active', target='suspended')
    def suspend(self, other):
        pass

    @transition(field=state, source='suspended', target='active')
    def reactivate(self, other):
        pass

    def save(self, *args, **kwargs):
        if False and not self.id:
            self.id = get_uuid()
            Identity.objects.create(identity=self)
            kwargs['force_insert'] = True
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
