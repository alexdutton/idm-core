from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from idm_core.attestation.models import Attestation
from idm_core.attestation.models import SourceDocument
from idm_core.name.models import Name
from idm_core.person.models import Person


class AttestationTestCase(TestCase):
    def testEditingAttested(self):
        # It shouldn't be possible to modify something that's attested
        person = Person.objects.create()
        user = get_user_model().objects.create(username='college-admin')
        name = Name.objects.create(person=person,
                                   components=[{'type': 'given', 'value': 'Alice'}])
        source_document = SourceDocument.objects.create(person=person,
                                                        type='visa',
                                                        validated_by=user)
        attestation = Attestation.objects.create(source_document=source_document,
                                                 attests=name)

        with self.assertRaises(ValidationError):
            name.components = [{'type': 'given', 'value': 'Bob'}]
            name.save()