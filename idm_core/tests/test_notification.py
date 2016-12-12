import json

import kombu
from django.db import transaction
from django.test import TransactionTestCase
from kombu.message import Message

from idm_core.identity.models import Identity
from idm_notification import broker


class NotificationTestCase(TransactionTestCase):
    fixtures = ['initial']

    def testPersonCreate(self):
        with broker.connection.acquire(block=True) as conn:
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.identity'), routing_key='#')
            with transaction.atomic():
                person = Identity(type_id='person')
                person.save()
            message = queue.get()
            self.assertIsInstance(message, Message)
            self.assertEqual(message.delivery_info['routing_key'],
                             'Person.created.{}'.format(str(person.id)))
            self.assertEqual(message.content_type, 'application/json')
            self.assertEqual(json.loads(message.body.decode())['@type'], 'Person')

    def testPersonCreateDelete(self):
        with broker.connection.acquire(block=True) as conn:
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.identity'), routing_key='#')
            with transaction.atomic():
                person = Identity(type_id='person')
                person.save()
                person.delete()
            message = queue.get()
            self.assertIsNone(message)

    def testNoNotifcationWhenNotChanged(self):
        with broker.connection.acquire(block=True) as conn:
            with transaction.atomic():
                person = Identity(type_id='person')
                person.save()
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.identity'), routing_key='#')
            with transaction.atomic():
                person.save()
            message = queue.get()
            self.assertIsNone(message)

    def testNotifcationWhenChanged(self):
        with broker.connection.acquire(block=True) as conn:
            with transaction.atomic():
                person = Identity(type_id='person')
                person.save()
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.identity'), routing_key='#')
            with transaction.atomic():
                person.extant = False
                person.save()
            message = queue.get()
            self.assertIsInstance(message, Message)
            self.assertEqual(message.delivery_info['routing_key'],
                             'Person.changed.{}'.format(str(person.id)))
            self.assertEqual(message.content_type, 'application/json')
            self.assertEqual(json.loads(message.body.decode())['deceased'], True)
