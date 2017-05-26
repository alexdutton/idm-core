import http.client

from django.test import TestCase

from idm_core.identifier.models import Identifier
from idm_core.person.models import Person


class SubViewTestCase(TestCase):
    fixtures = ['initial']

    def testIdentifierSubView(self):
        # Test that the IdentitySubViewMixin works and filters out identifiers for other identities
        person = Person.objects.create()
        identifier = Identifier.objects.create(identity=person,
                                               type_id='username',
                                               value='my_username')
        other_person = Person.objects.create()
        other_identifier = Identifier.objects.create(identity=other_person,
                                                     type_id='username',
                                                     value='other_username')
        response = self.client.get('/api/person/{}/identifier/'.format(person.id))
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['value'], identifier.value)
