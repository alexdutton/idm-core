from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.functional import cached_property

from idm_core.contact.mixins import Contactable
from idm_core.course.models import Course
from idm_core.identity.models import IdentityBase
from idm_core.person.models import Person
from idm_core.relationship.models import Relationship, RelationshipType


class OrganizationTag(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return '{} ({})'.format(self.id, self.label)


class OrganizationRelationshipType(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    label = models.CharField(max_length=255)


class Organization(IdentityBase):
    type_slug = 'organization'
    sub_nav_template = 'organization/sub_nav.html'

    short_label = models.CharField(max_length=255, blank=True)

    tags = models.ManyToManyField(OrganizationTag, blank=True)

    relationships = models.ManyToManyField(to='self', through='OrganizationRelationship', symmetrical=False)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('organization:detail', kwargs={'pk': str(self.id)})

    class Meta:
        permissions = (
            ('manage_organization', 'can manage an organization'),
            ('view_affiliations', 'can view affiliated people'),
            ('manage_affiliations', 'can manage affiliations'),
            ('offer_affiliations', 'can offer affiliations'),
            ('manage_roles', 'can manage roles'),
        )


class OrganizationRelationship(models.Model):
    type = models.ForeignKey(OrganizationRelationshipType)
    subject = models.ForeignKey(Organization, related_name='relationship')
    object = models.ForeignKey(Organization, related_name='incoming_relationship')


class RoleType(RelationshipType):
    """
    e.g. bursar, ITSS, information custodian
    """
    # Role, in w3c org ontology terms
    pass


class OrganizationRole(IdentityBase):
    type_slug = 'organization-role'

    organization = models.ForeignKey(Organization)
    role_type = models.ForeignKey(RoleType)
    role_label = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.label = self.role_label or self.role_type.label
        self.qualified_label = ', '.join([self.label, self.organization.label])
        self.sort_label = ', '.join([self.organization.label, self.label])
        return super().save(*args, **kwargs)


class Role(Relationship):
    identity = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(RoleType)

    @cached_property
    def organization_role(self):
        try:
            return OrganizationRole.objects.get(organization=self.organization, role_type=self.type)
        except OrganizationRole.DoesNotExist:
            return OrganizationRole.objects.create(organization=self.organization,
                                                   role_type=self.type)

    def save(self, *args, **kwargs):
        self.organization_role
        return super().save(*args, **kwargs)


class BodleianGroup(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    label = models.CharField(max_length=64)


class AffiliationType(RelationshipType):
    edu_person_affiliation_value = models.CharField(max_length=64, blank=True)
    metadata_fields = ArrayField(models.CharField(max_length=32), default=[])

    class Meta:
        ordering = ('label',)


class Affiliation(Relationship):
    identity = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(AffiliationType)
    order = models.PositiveSmallIntegerField()

    job_title = models.TextField(blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    bodleian_group = models.ForeignKey(BodleianGroup, null=True, blank=True)
    congregation_organization = models.ForeignKey(Organization, null=True, blank=True, related_name='congregation_affiliations')

    def get_absolute_url(self):
        return reverse('organization:affiliation-update', kwargs={'organization_pk': str(self.organization_id),
                                                                  'pk': str(self.id)})

    def save(self, *args, **kwargs):
        if self.state not in ('upcoming', 'active', 'suspended'):
            self.order = 10000
        elif self.order is None:
            c = type(self).objects.filter(identity_id=self.identity_id, state__in=('upcoming', 'active', 'suspended')).aggregate(Max('order')).get('order__max')
            self.order = 0 if c is None else c + 1
        return super().save(*args, **kwargs)

    class Meta(Relationship.Meta):
        ordering = ('order',)
