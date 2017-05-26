import http.client
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from idm_core.person.models import Person


class FiltersTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        user = get_user_model()(username=uuid.uuid4())
        user.set_password('password')
        user.save()
        self.client.login(username=user.username, password='password')

    def testCantSee(self):
        person = Person.objects.create()

        response = self.client.get('/api/person/')
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(data['count'], 0)

        response = self.client.get('/person/{}/'.format(person.id))
        self.assertEqual(response.status_code, http.client.NOT_FOUND)

