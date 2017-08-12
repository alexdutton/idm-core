from django.apps import apps, AppConfig
from django.conf import settings
from django.db import connection

from idm_core.identity.signals import post_merge


class IdentityConfig(AppConfig):
    name = 'idm_core.identity'
    verbose_name = 'Identities'

    def ready(self):
        post_merge.connect(self.on_post_merge)

    def on_post_merge(self, target, others, other_ids, **kwargs):
        connection.on_commit(lambda: self.publish_merge_to_amqp(target, others, other_ids))

    def publish_merge_to_amqp(self, target, others, other_ids):
        broker_app_config = apps.get_app_config('idm_broker')
        with broker_app_config.broker.acquire(block=True) as conn:
            producer = conn.Producer(serializer='json')
            producer.publish({'mergedIdentities': sorted(other_ids),
                              'targetIdentity': target.id},
                             exchange=settings.BROKER_PREFIX + type(target).__name__.lower(),
                             routing_key='{}.{}.{}'.format(type(target).__name__,
                                                           'merged',
                                                           target.pk))
