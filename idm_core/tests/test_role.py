from django.test import TestCase

from idm_core.relationship.models import Role, RoleType
from idm_core.organization.models import Organization
from idm_core.identity.models import Identity


class RoleTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        self.organization = Identity.objects.create(type_id='organization',
                                                    label='Department of Metaphysics')
        self.role_type = RoleType.objects.get(pk='head')

    def testCreateRole(self):
        person = Identity.objects.create(type_id='person')
        role = Role(identity=person,
                    target=self.organization,
                    type=self.role_type)
        role.save()
        self.assertEqual(Identity.objects.filter(type_id='organization-role',
                                                 organization=self.organization,
                                                 role_type=self.role_type).count(), 1)
