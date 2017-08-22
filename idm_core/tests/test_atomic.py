import http.client
import json
import uuid

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
import kombu
from rest_framework.test import APITransactionTestCase

from idm_core.person.models import Person


class AtomicityTestCase(APITransactionTestCase):
    fixtures = ['initial']

    def setUp(self):
        self.user = get_user_model()(username=uuid.uuid4(), is_superuser=True)
        self.client.force_authenticate(self.user)
        self.broker = apps.get_app_config('idm_broker').broker

    def testCreationAtomic(self):
        # Check that:
        # a) Creation takes place in a transaction.atomic() block, and
        # b) That this only fires a single notification

        is_atomic = None

        def check_is_atomic(**kwargs):
            nonlocal is_atomic
            connection = transaction.get_connection()
            if is_atomic is None:
                is_atomic = connection.in_atomic_block
            elif not connection.in_atomic_block:
                is_atomic = False

        try:
            post_save.connect(check_is_atomic, Person)

            with self.broker.acquire(block=True) as conn:
                queue = kombu.Queue(exclusive=True).bind(conn)
                queue.declare()
                queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')

                response = self.client.post('/api/person/', json.dumps({
                    'emails': [{
                        'context': 'home',
                        'value': 'user@example.org',
                    }]
                }), content_type='application/json')
                self.assertEqual(http.client.CREATED, response.status_code)

                self.assertTrue(is_atomic)

                person = Person.objects.get()

                message = queue.get()
                self.assertEqual(response.status_code, http.client.CREATED)
                self.assertIsInstance(message, kombu.Message)
                self.assertEqual(message.delivery_info['routing_key'],
                                 'Person.created.{}'.format(str(person.id)))

                message_body = json.loads(message.body.decode())
                self.assertEqual('user@example.org', message_body['emails'][0]['value'])

                # Make sure there are no further messages
                self.assertIsNone(queue.get())
        finally:
            post_save.disconnect(check_is_atomic, Person)
