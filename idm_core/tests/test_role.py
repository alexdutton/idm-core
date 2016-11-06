from django.test import TestCase

from idm_core.models import Person
from idm_core.org_relationship.models import Role, RoleType, OrganizationRole
from idm_core.organization.models import Organization


class RoleTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        self.organization = Organization.objects.create(label='Department of Metaphysics')
        self.role_type = RoleType.objects.get(pk='head')

    def testCreateRole(self):
        person = Person.objects.create()
        role = Role(person=person,
                    organization=self.organization,
                    type=self.role_type)
        role.save()
        self.assertEqual(OrganizationRole.objects.filter(organization=self.organization,
                                                         type=self.role_type).count(), 1)
