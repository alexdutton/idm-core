import http.client

from django.test import TestCase

from idm_core.identity.models import Identity


class IdentityTransitionTestCase(TestCase):
    fixtures = ['initial']

    def testActivate(self):
        identity = Identity.objects.create(type_id='person')
        response = self.client.post('/person/{}/activate/'.format(identity.id))
        self.assertEqual(response.status_code, http.client.OK)

        identity = Identity.objects.get()
        self.assertEqual(identity.state, 'active')

    def testArchive(self):
        identity = Identity.objects.create(type_id='person', state='active')
        response = self.client.post('/person/{}/archive/'.format(identity.id))
        self.assertEqual(response.status_code, http.client.OK)

        identity = Identity.objects.get()
        self.assertEqual(identity.state, 'archived')
