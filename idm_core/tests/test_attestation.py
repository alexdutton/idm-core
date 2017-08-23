import http.client
import uuid

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.test import TestCase

from idm_core.attestation.models import Attestation
from idm_core.attestation.models import SourceDocument
from idm_core.contact.models import Address, ContactContext
from idm_core.name.models import Name
from idm_core.person.models import Person


class AttestationTestCase(TestCase):
    fixtures = ['initial']

    def testEditingAttested(self):
        # It shouldn't be possible to modify something that's attested
        person = Person.objects.create()
        user = get_user_model().objects.create(username=uuid.uuid4())
        name = Name.objects.create(identity=person,
                                   components=[{'type': 'given', 'value': 'Alice'}],
                                   context_id='legal')
        source_document = SourceDocument.objects.create(identity=person,
                                                        type_id='visa',
                                                        validated_by=user)
        attestation = Attestation.objects.create(source_document=source_document,
                                                 attests=name)

        with self.assertRaises(ValidationError):
            name.components = [{'type': 'given', 'value': 'Bob'}]
            name.save()


class AttestationViewTestCase(TestCase):
    fixtures = ['initial']

    def testAttestableGet(self):
        person = Person.objects.create()
        name = Name.objects.create(identity=person,
                                   components=[{'type': 'given', 'value': 'Alice'}],
                                   context_id='legal')
        address = Address.objects.create(identity=person, context=ContactContext.objects.get(pk='home'))

        response = self.client.get('/api/person/{}/attestable/'.format(person.pk))

        self.assertEqual(response.status_code, http.client.OK)
        data = response.json()

        self.assertEqual(len(data['results']), 2)
        self.assertEqual({d['@type'] for d in data['results']}, {'Name', 'Address'})
