import http.client

from django.test import TestCase

from idm_core.identifier.models import Identifier
from idm_core.identity.models import Identity


class SubViewTestCase(TestCase):
    fixtures = ['initial']

    def testIdentifierSubView(self):
        # Test that the IdentitySubViewMixin works and filters out identifiers for other identities
        identity = Identity.objects.create(type_id='person')
        identifier = Identifier.objects.create(identity=identity,
                                         type_id='username',
                                         value='my_username')
        other_identity = Identity.objects.create(type_id='person')
        other_identifier = Identifier.objects.create(identity=other_identity,
                                                     type_id='username',
                                                     value='other_username')
        response = self.client.get('/person/{}/identifier/'.format(identity.id))
        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['value'], identifier.value)