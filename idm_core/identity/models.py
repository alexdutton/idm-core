import uuid

from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_fsm import FSMField, transition
import templated_email


# ISO/IEC 24760-1:2011
from idm_core.contact.mixins import Contactable
from idm_core.identifier.mixins import Identifiable

IDENTITY_STATE_CHOICES = (
    ('established', 'established'),
    ('active', 'active'),
    ('archived', 'archived'),
    ('suspended', 'suspended'),
    ('merged', 'merged'), # Not in standard, but used for operational purposes
)


class UserManager(BaseUserManager):
    def create_superuser(self, password, **kwargs):
        user = self.model(**kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()


class AbstractUserWithoutUsername(AbstractUser):
    class Meta:
        abstract = True
AbstractUserWithoutUsername._meta.local_fields.remove(AbstractUserWithoutUsername._meta.get_field('username'))


class User(AbstractUserWithoutUsername):
    username = models.UUIDField(db_index=True, unique=True, editable=False)
    principal_name = models.CharField(max_length=256, db_index=True, unique=True, null=True, blank=True)
    identity_id = models.UUIDField(null=True, blank=True)
    identity_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    objects = UserManager()

    def __str__(self):
        return str(self.username)

    def get_short_name(self):
        "Returns the short name for the user."
        try:
            return str(self.identity)
        except :
            return str(self.id)


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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    label = models.CharField(max_length=1024, blank=True)
    qualified_label = models.CharField(max_length=1024, blank=True)
    sort_label = models.CharField(max_length=1024, blank=True)

    primary_username = models.CharField(blank=True, max_length=32)

    state = FSMField(choices=IDENTITY_STATE_CHOICES, default='established')
    merged_into = models.ForeignKey('self', null=True, blank=True, related_name='merged_from')

    identity_permissions = GenericRelation('identity.IdentityPermission', 'identity_id', 'identity_content_type')
    source_documents = GenericRelation('attestation.SourceDocument', 'identity_id', 'identity_content_type')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
        super().save(*args, **kwargs)
        Identity.objects.get_or_create(id=self.id,
                                       content_type=ContentType.objects.get_for_model(type(self)))

    def __str__(self):
        return self.label

    class Meta:
        abstract = True


class IdentityPermission(models.Model):
    """The given identity has permissions to manage identities in the given organizations."""

    identity_content_type = models.ForeignKey(ContentType)
    identity_id = models.UUIDField()
    identity = GenericForeignKey('identity_content_type', 'identity_id')
    organizations = models.ManyToManyField('organization.Organization', blank=True)
    all_organizations = models.BooleanField(default=False)
    identifier_types = models.ManyToManyField('identifier.IdentifierType', blank=True)
    all_identifier_types = models.BooleanField(default=False)
