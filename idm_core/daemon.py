import uuid

import kombu
from django.apps import apps
from django.db import transaction, connection
from kombu.mixins import ConsumerMixin, logger

user_queue = kombu.Queue('idm.core.user',
                         exchange=kombu.Exchange('idm.auth.user', type='topic'),
                         auto_declare=True, routing_key='#')


class IDMCoreDaemon(ConsumerMixin):
    def __call__(self):
        idm_broker_config = apps.get_app_config('idm_broker')
        with idm_broker_config.broker.acquire(block=True) as conn:
            self.connection = conn
            self.run()

    def run(self, _tokens=1, **kwargs):
        try:
            super().run(_tokens=_tokens, **kwargs)
        finally:
            connection.close()

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[user_queue],
                         accept=['json'],
                         callbacks=[self.process_user],
                         auto_declare=True)]

    def process_user(self, body, message):
        from idm_core.identity.models import Identity, User

        with transaction.atomic(savepoint=False):
            assert isinstance(message, kombu.message.Message)
            _, action, id = message.delivery_info['routing_key'].split('.')
            id = uuid.UUID(id)
            if action in ('created', 'changed'):
                try:
                    user = User.objects.get(username=id)
                except User.DoesNotExist:
                    user = User(username=id)
                print(body)
                try:
                    identity = Identity.objects.get(id=body['identity_id'])
                except Identity.DoesNotExist:
                    logger.warning("Couldn't match identity for user {} (identity {})".format(body['id'], body['identity_id']))
                    message.reject()
                    return
                user.identity_id = identity.id
                user.identity_content_type = identity.content_type
                user.principal_name = body['principal_name']
                user.save()
                message.ack()
                logger.info("User {}".format(action))
            elif action == 'deleted':
                for user in User.objects.filter(id=id):
                    user.delete()
                message.ack()
            else:
                message.reject()
