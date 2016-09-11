from urllib.parse import urljoin

import collections
import enum
import kombu
from django.conf import settings

from django.db import connection
from django.db.models.signals import post_save, post_delete, pre_delete

from oxidentity.gender.models import Gender
from oxidentity.gender.serializers import GenderSerializer
from oxidentity.identifier.models import IdentifierType
from oxidentity.identifier.serializers import IdentifierTypeSerializer
from oxidentity.models import Identity
from oxidentity.nationality.models import Country
from oxidentity.nationality.serializers import CountrySerializer
from oxidentity.org_relationship.models import Affiliation, Role, AffiliationType, RoleType, Unit
from oxidentity.org_relationship.serializers import AffiliationSerializer, RoleSerializer, RoleTypeSerializer, \
    AffiliationTypeSerializer, UnitSerializer
from oxidentity.serializers import IdentitySerializer

INITIAL_FIELD_VALUES = '_initial_field_values'
NEEDS_PUBLISH = '_needs_publish'

_ModelConfig = collections.namedtuple('_ModelConfig', 'serializer exchange natural_key')

reference_exchange = kombu.Exchange('iam.idm.reference', 'topic', durable=True)

_model_config = {
    Identity: _ModelConfig(IdentitySerializer,
                           kombu.Exchange('iam.idm.identity', 'topic', durable=True),
                           lambda instance: instance.uuid),
    Affiliation: _ModelConfig(AffiliationSerializer,
                              kombu.Exchange('iam.idm.affiliation', 'topic', durable=True),
                              lambda instance: instance.identity_id),
    Role: _ModelConfig(RoleSerializer,
                       kombu.Exchange('iam.idm.role', 'topic', durable=True),
                       lambda instance: instance.identity_id),
}

reference_models = [
    (AffiliationType, AffiliationTypeSerializer),
    (RoleType, RoleTypeSerializer),
    (IdentifierType, IdentifierTypeSerializer),
    (Gender, GenderSerializer),
    (Country, CountrySerializer),
    (Unit, UnitSerializer),
]

for model, serializer in reference_models:
    _model_config[model] = _ModelConfig(serializer, reference_exchange,
                                        lambda instance: '{}.{}'.format(type(instance).__name__, instance.pk))

class _FakeRequest(object):
    def build_absolute_uri(self, url):
        return urljoin(settings.API_BASE, url)

    GET = {}


amqp_connection = kombu.Connection(settings.BROKER_URL)


def publish_model_change_to_amqp(sender, instance, **kwargs):
    model_config = _model_config[sender]

    needs_publish = instance._needs_publish
    instance._needs_publish = set()

    if 'created' in needs_publish and 'deleted' in needs_publish:
        return
    elif 'deleted' in needs_publish:
        publish_type = 'deleted'
    elif 'created' in needs_publish:
        publish_type = 'created'
    else:
        publish_type = 'changed'

    serializer = model_config.serializer(context={'request': _FakeRequest()})

    with kombu.producers[amqp_connection].acquire(block=True) as producer:
        producer.publish(serializer.to_representation(instance),
                         exchange=model_config.exchange,
                         routing_key='{}.{}'.format(publish_type,
                                                    model_config.natural_key(instance)),
                         declare=[model_config.exchange])




def instance_changed(sender, instance, created, **kwargs):
    if sender not in _model_config:
        return
    publish_type = 'created' if created else 'changed'
    try:
        instance._needs_publish.add(publish_type)
    except AttributeError:
        instance._needs_publish = {publish_type}
    connection.on_commit(lambda : publish_model_change_to_amqp(sender, instance))

post_save.connect(instance_changed)


def instance_deleted(sender, instance, **kwargs):
    if sender not in _model_config:
        return
    try:
        instance._needs_publish.add('deleted')
    except AttributeError:
        instance._needs_publish = {'deleted'}
    connection.on_commit(lambda : publish_model_change_to_amqp(sender, instance))

pre_delete.connect(instance_deleted)


def publish_merge_to_amqb(merge_these, into_this):
    model_config = _model_config[Identity]
    with kombu.Connection(settings.BROKER_URL) as conn:
        producer = conn.Producer(serializer='json')
        producer.publish({'mergedIdentities': [identity.id for identity in merge_these],
                          'targetIdentity': into_this.id},
                         exchange=model_config.exchange,
                         routing_key='{}.{}'.format('merged',
                                                    getattr(into_this, model_config.natural_key)))
