from django.db import IntegrityError
from django.test import TestCase

from idm_core.contact.models import ContactContext, Email
from idm_core.person.models import Person


class ContactTestCase(TestCase):
    fixtures = ['initial']

    def testDuplicateUnvalidatedEmail(self):
        identity = Person.objects.create()
        email_one = Email.objects.create(identity=identity,
                                         context=ContactContext.objects.get(pk='home'),
                                         validated=True)
        email_two = Email.objects.create(identity=identity,
                                         context=ContactContext.objects.get(pk='home'),
                                         validated=False)
        self.assertEqual(Email.objects.count(), 2)

    def testDuplicateValidatedEmail(self):
        identity = Person.objects.create()
        email_one = Email.objects.create(identity=identity,
                                         context=ContactContext.objects.get(pk='home'),
                                         validated=True)
        with self.assertRaises(IntegrityError):
            email_two = Email.objects.create(identity=identity,
                                             context=ContactContext.objects.get(pk='home'),
                                             validated=True)
