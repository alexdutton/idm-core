from django.test import TransactionTestCase

from idm_core import merging
from idm_core.person.models import Person
from idm_core.person.serializers import PersonSerializer


class MergingTestCase(TransactionTestCase):
    fixtures = ['initial']

    def create_person_from_json(self, data):
        serializer = PersonSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def testSimpleMerge(self):
        primary = Person.objects.create()
        secondary = Person.objects.create()

        merging.merge(secondary, primary)

        self.assertEqual(secondary.merged_into, primary)
        self.assertEqual(secondary.state, 'merged')

    def testEverythingMoved(self):
        primary = self.create_person_from_json({
            'names': [{
                "contexts": ["legal"],
                "components": [{"type": "given", "value": "Alice"}],
            }],
            'identifiers': [{
                "type": "username",
                "value": "abcd0001",
            }],
        })
        secondary = self.create_person_from_json({
            'names': [{
                "contexts": ["presentational"],
                "components": [{"type": "given", "value": "Bob"}],
            }],
            'identifiers': [{
                "type": "username",
                "value": "abcd0002",
            }],
        })

        merging.merge(secondary, primary)

        self.assertEqual(primary.names.count(), 2)
        self.assertEqual(secondary.names.count(), 0)

        self.assertEqual(primary.identifiers.count(), 2)
        self.assertEqual(secondary.identifiers.count(), 0)
