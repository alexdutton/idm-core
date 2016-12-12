from django.test import TestCase

from idm_core.identifier.models import Identifier
from idm_core.identity.models import Identity


class IdentifierTestCase(TestCase):
    fixtures = ['initial']

    def testFindByIdentifier(self):
        identity = Identity.objects.create(type_id='person')
        identifier = Identifier.objects.create(identity=identity,
                                               type_id='sits-mst',
                                               value='123456')
        #self.client.get()