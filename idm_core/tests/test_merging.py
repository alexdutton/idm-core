from django.test import TransactionTestCase

from idm_core import merging
from idm_core.person.models import Person


class MergingTestCase(TransactionTestCase):
    def testSimpleMerge(self):
        primary = Person.objects.create()
        secondary = Person.objects.create()

        merging.merge(secondary, primary)
