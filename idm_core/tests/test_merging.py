import datetime

from django.test import TransactionTestCase

from idm_core.identity import merging
from idm_core.identity.merging import MergeTypeDisparity
from idm_core.identity.models import Identity
from idm_core.identity.serializers import PersonSerializer


class MergingTestCase(TransactionTestCase):
    fixtures = ['initial']

    def create_person_from_json(self, data):
        serializer = PersonSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def testSimpleMerge(self):
        primary = Identity.objects.create(type_id='person')
        secondary = Identity.objects.create(type_id='person')

        merging.merge(secondary, primary)

        self.assertEqual(secondary.merged_into, primary)
        self.assertEqual(secondary.state, 'merged')

    def testCantMergeDifferentTypes(self):
        primary = Identity.objects.create(type_id='person')
        secondary = Identity.objects.create(type_id='organization')

        with self.assertRaises(MergeTypeDisparity):
            merging.merge(secondary, primary)


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
            'sex': '2',
            'date_of_birth': '1970-01-02',
            'date_of_death': '1970-01-03',
        })

        merging.merge(secondary, primary)

        self.assertEqual(primary.names.count(), 2)
        self.assertEqual(secondary.names.count(), 0)

        self.assertEqual(primary.identifiers.count(), 2)
        self.assertEqual(secondary.identifiers.count(), 0)

        self.assertEqual(primary.sex, '2')
        self.assertEqual(primary.begin_date, datetime.date(1970, 1, 2))
        self.assertEqual(primary.end_date, datetime.date(1970, 1, 3))

    def testDontDuplicateNationalities(self):
        primary = self.create_person_from_json({
            'names': [{
                "contexts": ["legal"],
                "components": [{"type": "given", "value": "Alice"}],
            }],
            'nationalities': [{
                "country": "GBR",
            }],
        })
        secondary = self.create_person_from_json({
            'names': [{
                "contexts": ["presentational"],
                "components": [{"type": "given", "value": "Bob"}],
            }],
            'nationalities': [{
                "country": "GBR",
            }],
        })

        merging.merge(secondary, primary)

        self.assertEqual(primary.nationalities.count(), 1)
        self.assertEqual(secondary.nationalities.count(), 0)