import http.client
import json
from unittest import mock
from django.test import TestCase
from django_fsm import TransitionNotAllowed

from idm_core.contact.models import Email, ContactContext
from idm_core.models import Identity


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
