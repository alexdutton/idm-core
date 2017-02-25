import http.client

from django.contrib.auth import get_user_model
from django.test import TestCase

from idm_core.person.models import Person


class IdentityTransitionTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        user = get_user_model()(is_superuser=True)
        user.set_password('admin')
        user.save()
        self.client.login(username=user.id, password='admin')

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
