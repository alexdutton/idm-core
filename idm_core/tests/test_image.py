from django.test import TestCase

from idm_core.image.models import Image, ImageContext
from idm_core.person.models import Person


class ImageModelTestCase(TestCase):
    context_id = 'card'

    def setUp(self):
        self.identity = Person.objects.create()
        self.approval_context = ImageContext.objects.create(id='approval', subject_to_acceptance=True)
        self.simple_context = ImageContext.objects.create(id='simple', subject_to_acceptance=False)

    def testCreateAndAccept(self):
        image = Image.objects.create(context=self.approval_context, identity=self.identity)
        self.assertEqual(image.state, 'proposed')
        image.accept()
        self.assertEqual(image.state, 'accepted')

    def testCreateAndAcceptWithOther(self):
        other_image = Image.objects.create(context=self.approval_context, state='accepted', identity=self.identity)
        image = Image.objects.create(context=self.approval_context, identity=self.identity)
        self.assertEqual(image.state, 'proposed')
        image.accept()
        self.assertEqual(image.state, 'accepted')
