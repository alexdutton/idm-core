from unittest import mock
from django.test import TestCase
from django_fsm import TransitionNotAllowed

from idm_core.contact.models import Email, ContactContext
from idm_core.models import Identity


class ClaimTestCase(TestCase):
    fixtures = ['initial']

    @mock.patch('templated_email.send_templated_mail')
    def testEmailSentOnStateChange(self, send_templated_mail):
        identity = Identity.objects.create()
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(identity=identity, context=contact_context, value='user@example.org')
        email.save()

        assert not send_templated_mail.called
        identity.ready_for_claim()
        self.assertEqual(send_templated_mail.call_count, 1)

    def testStateChangeFailWithoutEmail(self):
        identity = Identity.objects.create()
        with self.assertRaises(TransitionNotAllowed):
            identity.ready_for_claim()

    @mock.patch('templated_email.send_templated_mail')
    def testCanBeClaimed(self, send_templated_mail):
        identity = Identity.objects.create()
        contact_context = ContactContext.objects.get(pk='home')
        email = Email(identity=identity, context=contact_context, value='user@example.org')
        email.save()

        identity.ready_for_claim()
        identity.claimed()
        self.assertEqual(identity.state, 'active')