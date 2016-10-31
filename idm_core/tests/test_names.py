from django.test import TestCase

from idm_core.models import Identity
from idm_core.name.models import NameContext, Name


class NamesTestCase(TestCase):
    fixtures = ['initial']

    def testSimpleName(self):
        identity = Identity.objects.create()
        name = Name(identity=identity,
                    components=[{'type': 'mononym', 'value': 'Socrates'}])
        name.save()
        self.assertEqual(str(name), 'Socrates')
        self.assertEqual(name.plain, 'Socrates')
        self.assertEqual(name.plain_full, 'Socrates')
        self.assertEqual(name.familiar, 'Socrates')
        self.assertEqual(name.marked_up, '<name><mononym>Socrates</mononym></name>')
