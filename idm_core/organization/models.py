from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from idm_core.contact.mixins import Contactable
from idm_core.identity.models import IdentityBase
from idm_core.person.models import Person
from idm_core.relationship.models import Relationship, RelationshipType


class OrganizationTag(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)


class OrganizationRelationshipType(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)


class Organization(IdentityBase):
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


class AffiliationType(RelationshipType):
    edu_person_affiliation_value = models.CharField(max_length=32, blank=True)


class Affiliation(Relationship):
    identity = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(AffiliationType)

    def get_absolute_url(self):
        return reverse('organization:affiliation-update', kwargs={'organization_pk': str(self.organization_id),
                                                                  'pk': str(self.id)})

    #metadata = JSONField(default={})
    # location
