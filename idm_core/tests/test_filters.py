import http.client
import uuid

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from idm_core.identifier.models import Identifier
from idm_core.organization.models import Organization, Affiliation
from idm_core.person.models import Person


class FiltersTestCase(APITestCase):
    fixtures = ['initial']

    def setUp(self):
        self.user = get_user_model()(username=uuid.uuid4(), is_superuser=True)
        self.client.force_authenticate(self.user)

    def testFilterByIdentifier(self):
        other_identity = Person.objects.create()
        identity = Person.objects.create()
        identifier = Identifier.objects.create(identity=identity,
                                               type_id='sits:mst',
                                               value='123456')

        response = self.client.get('/api/person/?identifierType=sits:mst&identifier=123456')
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['id'], str(identity.id))

    def testFilterByAffiliation(self):
        other_identity = Person.objects.create()
        identity = Person.objects.create()
        organization = Organization.objects.create()
        affiliation = Affiliation.objects.create(identity=identity,
                                                 organization=organization,
                                                 type_id='staff',
                                                 state='active')

        response = self.client.get('/api/person/', {'affiliationOrganization': organization.id})
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['id'], str(identity.id))
