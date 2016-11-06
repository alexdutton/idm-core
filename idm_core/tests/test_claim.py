from unittest import mock

from django.test import TestCase
from django_fsm import TransitionNotAllowed

from idm_core.contact.models import Email, ContactContext
from idm_core.person.models import Person


class ClaimTestCase(TestCase):
    fixtures = ['initial']

    @mock.patch('templated_email.send_templated_mail')
    def testEmailSentOnStateChange(self, send_templated_mail):
        person = Person.objects.create()
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(person=person, context=contact_context, value='user@example.org')
        email.save()

        assert not send_templated_mail.called
        person.ready_for_claim()
        self.assertEqual(send_templated_mail.call_count, 1)

    def testStateChangeFailWithoutEmail(self):
        person = Person.objects.create()
        with self.assertRaises(TransitionNotAllowed):
            person.ready_for_claim()

    @mock.patch('templated_email.send_templated_mail')
    def testCanBeClaimed(self, send_templated_mail):
        person = Person.objects.create()
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(person=person, context=contact_context, value='user@example.org')
        email.save()

        person.ready_for_claim()
        person.claimed()
        self.assertEqual(person.state, 'active')
