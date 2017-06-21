import http.client
import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from idm_core.person.models import Person


class FiltersTestCase(APITestCase):
    fixtures = ['initial']

    def setUp(self):
        self.user = get_user_model()(username=uuid.uuid4())
        self.client.force_authenticate(self.user)

    def testCantSee(self):
        person = Person.objects.create()

        response = self.client.get('/api/person/')
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(data['count'], 0)

        response = self.client.get('/person/{}/'.format(person.id))
        self.assertEqual(response.status_code, http.client.NOT_FOUND)

