from django.test import TestCase

from idm_core.application.models import Application
from idm_core.identity.models import Identity


class IdentityTestCase(TestCase):
    def testIdentityCreated(self):
        application = Application.objects.create()
        identity = Identity.objects.get(id=application.id)
        self.assertEqual(application, identity.identity)
