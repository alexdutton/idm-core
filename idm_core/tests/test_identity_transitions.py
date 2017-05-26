import http.client
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from idm_core.person.models import Person


class IdentityTransitionTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        user = get_user_model()(username=uuid.uuid4(), is_superuser=True)
        user.set_password('admin')
        user.save()
        self.client.login(username=user.username, password='admin')

    def testActivate(self):
        person = Person.objects.create()
        response = self.client.post('/api/person/{}/activate/'.format(person.id))
        self.assertEqual(response.status_code, http.client.OK)

        person = Person.objects.get()
        self.assertEqual(person.state, 'active')

    def testArchive(self):
        person = Person.objects.create(state='active')
        response = self.client.post('/api/person/{}/archive/'.format(person.id))
        self.assertEqual(response.status_code, http.client.OK)

        person = Person.objects.get()
        self.assertEqual(person.state, 'archived')
