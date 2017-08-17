from django.test import TestCase

from idm_core.image.models import Image, ImageContext
from idm_core.person.models import Person


class ImageModelTestCase(TestCase):
    context_id = 'card'

    def setUp(self):
        self.identity = Person.objects.create()
        self.approval_context = ImageContext.objects.create(id='approval', subject_to_approval=True)
        self.simple_context = ImageContext.objects.create(id='simple', subject_to_approval=False)

    def testCreateAndApprove(self):
        image = Image.objects.create(context=self.approval_context, identity=self.identity)
        self.assertEqual(image.state, 'proposed')
        image.approve()
        self.assertEqual(image.state, 'approved')

    def testCreateAndApproveWithOther(self):
        other_image = Image.objects.create(context=self.approval_context, state='approved', identity=self.identity)
        image = Image.objects.create(context=self.approval_context, identity=self.identity)
        self.assertEqual(image.state, 'proposed')
        image.approve()
        self.assertEqual(image.state, 'approved')
