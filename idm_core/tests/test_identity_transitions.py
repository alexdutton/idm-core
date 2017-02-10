import http.client

from django.test import TestCase

from idm_core.person.models import Person


class IdentityTransitionTestCase(TestCase):
    fixtures = ['initial']

    def testActivate(self):
        person = Person.objects.create()
        response = self.client.post('/person/{}/activate/'.format(person.id))
        self.assertEqual(response.status_code, http.client.OK)

        person = Person.objects.get()
        self.assertEqual(person.state, 'active')

    def testArchive(self):
        person = Person.objects.create(state='active')
        response = self.client.post('/person/{}/archive/'.format(person.id))
        self.assertEqual(response.status_code, http.client.OK)

        person = Person.objects.get()
        self.assertEqual(person.state, 'archived')
