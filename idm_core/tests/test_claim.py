from unittest import mock

from django.test import TestCase
from django_fsm import TransitionNotAllowed

from idm_core.contact.models import Email, ContactContext
from idm_core.identity.models import Identity


class ClaimTestCase(TestCase):
    fixtures = ['initial']

    @mock.patch('templated_email.send_templated_mail')
    def testEmailSentOnStateChange(self, send_templated_mail):
        person = Identity.objects.create(type_id='person')
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(identity=person, context=contact_context, value='user@example.org')
        email.save()

        assert not send_templated_mail.called
        person.ready_for_activation()
        self.assertEqual(send_templated_mail.call_count, 1)

    def testStateChangeFailWithoutEmail(self):
        person = Identity.objects.create(type_id='person')
        with self.assertRaises(TransitionNotAllowed):
            person.ready_for_activation()

    @mock.patch('templated_email.send_templated_mail')
    def testCanBeClaimed(self, send_templated_mail):
        person = Identity.objects.create(type_id='person')
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(identity=person, context=contact_context, value='user@example.org')
        email.save()

        person.ready_for_activation()
        person.activate()
        self.assertEqual(person.state, 'active')
