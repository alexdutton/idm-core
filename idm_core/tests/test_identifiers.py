from django.test import TestCase

from idm_core.identifier.models import Identifier
from idm_core.identity.models import Identity
from idm_core.person.models import Person


class IdentifierTestCase(TestCase):
    fixtures = ['initial']

    def testFindByIdentifier(self):
        identity = Person.objects.create()
        identifier = Identifier.objects.create(identity=identity,
                                               type_id='sits-mst',
                                               value='123456')
        #self.client.get()