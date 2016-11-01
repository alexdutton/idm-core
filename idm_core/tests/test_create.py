import http.client
import json
from unittest import mock
from django.test import TestCase
from django_fsm import TransitionNotAllowed

from idm_core.contact.models import Email, ContactContext
from idm_core.models import Identity
from idm_core.name.models import NameContext


class CreationTestCase(TestCase):
    fixtures = ['initial']

    def testCreate(self):
        response = self.client.post('/identity/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        identity_id = data['id']
        identity = Identity.objects.get(id=identity_id)
        self.assertEqual(identity.state, 'new')

    def testCreateWithEmail(self):
        response = self.client.post('/identity/', json.dumps({
            'emails': [{
                'context': 'home',
                'value': 'user@example.org',
            }]
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        identity_id = data['id']
        identity = Identity.objects.get(id=identity_id)
        self.assertEqual(identity.emails.count(), 1)
        email = identity.emails.get()
        self.assertEqual(email.context, ContactContext.objects.get(pk='home'))
        self.assertEqual(email.value, 'user@example.org')

    def testCreateWithNames(self):
        name_components = [{'type': 'given', 'value': 'Charles'},
                           {'type': 'middle', 'value': 'Robert'},
                           {'type': 'family', 'value': 'Darwin'}]
        response = self.client.post('/identity/', json.dumps({
            'names': [{
                'contexts': ['legal'],
                'components': name_components,
            }]
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        identity_id = data['id']
        identity = Identity.objects.get(id=identity_id)
        self.assertEqual(identity.names.count(), 1)
        name = identity.names.get()
        self.assertEqual(list(name.contexts.all()), [NameContext.objects.get(pk='legal')])
        self.assertEqual(name.components, name_components)

    def testCreateWithNationalities(self):
        nationalities = [{'country': 'GBR'}, {'country': 'US'}, {'country': '535'}, {'country': 800}]
        response = self.client.post('/identity/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        identity_id = data['id']
        identity = Identity.objects.get(id=identity_id)
        self.assertEqual(identity.nationalities.count(), 4)
        nationalities = identity.nationality_set.all()
        self.assertEqual(set(n.country.id for n in nationalities), {826, 840, 535, 800})

    def testCreateWithUnknownNationality(self):
        nationalities = [{'country': 'XYZ'}]
        response = self.client.post('/identity/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreateWithMalformedNationality(self):
        nationalities = [{'country': 'ABCD'}]
        response = self.client.post('/identity/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreateWithMissingNationality(self):
        nationalities = [{}]
        response = self.client.post('/identity/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreatePendingClaim(self):
        # This shouldn't be possible. Either create as active, or create as new and set as pending_claim
        response = self.client.post('/identity/', json.dumps({'state': 'pending_claim'}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)