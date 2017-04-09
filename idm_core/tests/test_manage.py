import http.client
import json
import unittest

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from idm_core.application.models import Application, ApplicationMayManageContentType
from idm_core.organization.models import Organization
from idm_core.person.models import Person
from idm_core.relationship.models import Affiliation


@unittest.skip('Tested functionality still a work in progress')
class ManageableTestCase(TestCase):
    """Test cases for the Manageable mixin and friends, which allows an Application to manage resources to the
    exclusion of other identities."""
    fixtures = ['initial']

    def setUp(self):
        self.application_a = Application.objects.create()
        self.application_b = Application.objects.create()
        ApplicationMayManageContentType.objects.create(application=self.application_a,
                                                       content_type=ContentType.objects.get_for_model(Affiliation))
        ApplicationMayManageContentType.objects.create(application=self.application_b,
                                                       content_type=ContentType.objects.get_for_model(Affiliation))
        self.user_a = get_user_model()(identity=self.application_a)
        self.user_a.set_password('password')
        self.user_a.save()
        self.user_b = get_user_model()(identity=self.application_b)
        self.user_b.set_password('password')
        self.user_b.save()
        self.person = Person.objects.create()
        self.organization = Organization.objects.create()

    def testUnmanaged(self):
        self.client.login(username=self.user_a.id, password='password')

        response = self.client.post('/affiliation/', {'identity_id': self.person.id,
                                                      'organization_id': self.organization.id,
                                                      'type_id': 'staff'})
        self.assertEqual(response.status_code, http.client.CREATED)
        affiliation_id = response.json()['id']

        self.client.login(username=self.user_b.id, password='password')
        response = self.client.put('/affiliation/{}/'.format(affiliation_id),
                                   json.dumps({'identity_id': str(self.person.id),
                                               'organization_id': str(self.organization.id),
                                               'type_id': 'friend'}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.OK)

    def testManaged(self):
        self.client.login(username=self.user_a.id, password='password')

        response = self.client.post('/affiliation/',
                                    json.dumps({'identity_id': str(self.person.id),
                                                'organization_id': str(self.organization.id),
                                                'type_id': 'staff',
                                                'managed': True}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        affiliation_id = response.json()['id']
        affiliation = Affiliation.objects.get(id=affiliation_id)
        self.assertEqual(affiliation.managed_by_id, self.application_a.id)

        self.client.login(username=self.user_b.id, password='password')
        response = self.client.put('/affiliation/{}/'.format(affiliation_id),
                                   json.dumps({'identity_id': str(self.person.id),
                                               'organization_id': str(self.organization.id),
                                               'type_id': 'friend'}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.FORBIDDEN)
        affiliation = Affiliation.objects.get(id=affiliation_id)
        self.assertEqual(affiliation.type_id, 'staff')

