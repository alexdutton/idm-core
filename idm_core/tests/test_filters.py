import http.client

from django.test import TestCase

from idm_core.identifier.models import Identifier
from idm_core.person.models import Person


class FiltersTestCase(TestCase):
    fixtures = ['initial']

    def testFilterByIdentifier(self):
        other_identity = Person.objects.create()

        identity = Person.objects.create()
        identifier = Identifier.objects.create(identity=identity,
                                               type_id='sits-mst',
                                               value='123456')

        response = self.client.get('/person/?identifierType=sits-mst&identifier=123456')
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)