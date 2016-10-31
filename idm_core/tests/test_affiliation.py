import datetime

from django.utils import timezone
from django.test import TestCase

from idm_core.models import Identity
from idm_core.org_relationship.models import AffiliationType, Affiliation
from idm_core.organization.models import Organization


class CreationTestCase(TestCase):
    fixtures = ['initial']

    def setUp(self):
        self.organization = Organization.objects.create(label='Department of Metaphysics')
        self.affiliation_type = AffiliationType.objects.get(pk='staff')

    def testForthcomingAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() + datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'forthcoming')

    def testActiveAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'active')

    def testHistoricAffiliation(self):
        identity = Identity.objects.create()
        affiliation = Affiliation(identity=identity,
                                  organization=self.organization,
                                  start_date=timezone.now() - datetime.timedelta(2),
                                  end_date=timezone.now() - datetime.timedelta(1),
                                  type=self.affiliation_type)
        affiliation.save()
        self.assertEqual(affiliation.state, 'historic')

