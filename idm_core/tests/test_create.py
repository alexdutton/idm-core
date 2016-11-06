import http.client
import json

from django.test import TestCase

from idm_core.contact.models import ContactContext
from idm_core.identifier.models import IdentifierType
from idm_core.name.models import NameContext
from idm_core.person.models import Person


class CreationTestCase(TestCase):
    fixtures = ['initial']

    def testCreate(self):
        response = self.client.post('/person/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        person_id = data['id']
        person = Person.objects.get(id=person_id)
        self.assertEqual(person.state, 'new')

    def testCreateWithEmail(self):
        response = self.client.post('/person/', json.dumps({
            'emails': [{
                'context': 'home',
                'value': 'user@example.org',
            }]
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        person_id = data['id']
        person = Person.objects.get(id=person_id)
        self.assertEqual(person.emails.count(), 1)
        email = person.emails.get()
        self.assertEqual(email.context, ContactContext.objects.get(pk='home'))
        self.assertEqual(email.value, 'user@example.org')

    def testCreateWithNames(self):
        name_components = [{'type': 'given', 'value': 'Charles'},
                           {'type': 'middle', 'value': 'Robert'},
                           {'type': 'family', 'value': 'Darwin'}]
        response = self.client.post('/person/', json.dumps({
            'names': [{
                'contexts': ['legal'],
                'components': name_components,
            }]
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        person_id = data['id']
        person = Person.objects.get(id=person_id)
        self.assertEqual(person.names.count(), 1)
        name = person.names.get()
        self.assertEqual(list(name.contexts.all()), [NameContext.objects.get(pk='legal')])
        self.assertEqual(name.components, name_components)

    def testCreateWithNationalities(self):
        nationalities = [{'country': 'GBR'}, {'country': 'US'}, {'country': '535'}, {'country': 800}]
        response = self.client.post('/person/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        person_id = data['id']
        person = Person.objects.get(id=person_id)
        self.assertEqual(person.nationalities.count(), 4)
        nationalities = person.nationality_set.all()
        self.assertEqual(set(n.country.id for n in nationalities), {826, 840, 535, 800})

    def testCreateWithIdentifier(self):
        response = self.client.post('/person/', json.dumps({
            'identifiers': [{
                'type': 'sits-mst',
                'value': '123456',
            }],
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.CREATED)
        data = response.json()
        person_id = data['id']
        person = Person.objects.get(id=person_id)
        identifier = person.identifiers.get()
        self.assertEqual(identifier.type, IdentifierType.objects.get(pk='sits-mst'))
        self.assertEqual(identifier.value, '123456')

    def testCreateWithUnknownNationality(self):
        nationalities = [{'country': 'XYZ'}]
        response = self.client.post('/person/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreateWithMalformedNationality(self):
        nationalities = [{'country': 'ABCD'}]
        response = self.client.post('/person/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreateWithMissingNationality(self):
        nationalities = [{}]
        response = self.client.post('/person/', json.dumps({
            'nationalities': nationalities,
        }), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)

    def testCreatePendingClaim(self):
        # This shouldn't be possible. Either create as active, or create as new and set as pending_claim
        response = self.client.post('/person/', json.dumps({'state': 'pending_claim'}), content_type='application/json')
        self.assertEqual(response.status_code, http.client.BAD_REQUEST)
