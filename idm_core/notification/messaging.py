import json
from urllib.parse import urljoin

import collections
import kombu
from django.conf import settings
from django.db import connection

from idm_core import broker
from idm_core.identifier.models import IdentifierType
from idm_core.identifier.serializers import IdentifierTypeSerializer
from idm_core.nationality.models import Country
from idm_core.nationality.serializers import CountrySerializer
from idm_core.org_relationship.models import Affiliation, Role, AffiliationType, RoleType, Organization
from idm_core.org_relationship.serializers import AffiliationSerializer, RoleSerializer, RoleTypeSerializer, \
    AffiliationTypeSerializer, OrganizationSerializer
from idm_core.organization.models import OrganizationTag
from idm_core.person.models import Person
from idm_core.person.serializers import PersonSerializer
from idm_core.settings import BROKER_PREFIX

INITIAL_FIELD_VALUES = '_initial_field_values'
NEEDS_PUBLISH = '_needs_publish'

_ModelConfig = collections.namedtuple('_ModelConfig', 'serializer exchange natural_key')

reference_exchange = kombu.Exchange(BROKER_PREFIX + 'reference', 'topic', durable=True)

_model_config = {
    Person: _ModelConfig(PersonSerializer,
                         kombu.Exchange(BROKER_PREFIX + 'person', 'topic', durable=True),
                         lambda instance: instance.id),
    Affiliation: _ModelConfig(AffiliationSerializer,
                              kombu.Exchange(BROKER_PREFIX + 'affiliation', 'topic', durable=True),
                              lambda instance: instance.person_id),
    Role: _ModelConfig(RoleSerializer,
                       kombu.Exchange(BROKER_PREFIX + 'role', 'topic', durable=True),
                       lambda instance: instance.person_id),
}

publish_related = {
    OrganizationTag: lambda organization_tag: organization_tag.organization_set.all(),

}

reference_models = [
    (AffiliationType, AffiliationTypeSerializer),
    (RoleType, RoleTypeSerializer),
    (IdentifierType, IdentifierTypeSerializer),
    (Country, CountrySerializer),
    (Organization, OrganizationSerializer),
]

for model, serializer in reference_models:
    _model_config[model] = _ModelConfig(serializer, reference_exchange,
                                        lambda instance: '{}.{}'.format(type(instance).__name__, instance.pk))

class _FakeRequest(object):
    def build_absolute_uri(self, url):
        return urljoin(settings.API_BASE, url)

    GET = {}


def init():
    with broker.connection.acquire(block=True) as connection:
        for mc in _model_config.values():
            exchange = mc.exchange(connection)
            exchange.declare()


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

    with broker.connection.acquire(block=True) as connection:
        exchange = model_config.exchange(connection)
        exchange.publish(exchange.Message(json.dumps(serializer.to_representation(instance)),
                                          content_type='application/json'),
                         routing_key='{}.{}'.format(publish_type,
                                                    model_config.natural_key(instance)))


def needs_publish(instance, publish_type):
    sender = type(instance)
    assert sender in _model_config
    try:
        instance._needs_publish.add(publish_type)
    except AttributeError:
        instance._needs_publish = {publish_type}
    connection.on_commit(lambda : publish_model_change_to_amqp(sender, instance))


def instance_changed(sender, instance, created, **kwargs):
    if sender not in _model_config:
        return
    publish_type = 'created' if created else 'changed'
    needs_publish(instance, publish_type)


def instance_deleted(sender, instance, **kwargs):
    if sender not in _model_config:
        return
    needs_publish(instance, 'deleted')


def publish_merge_to_amqp(merge_these, into_this):
    model_config = _model_config[Person]
    with broker.Connection(settings.BROKER_URL) as conn:
        producer = conn.Producer(serializer='json')
        producer.publish({'mergedIdentities': [person.id for person in merge_these],
                          'targetPerson': into_this.id},
                         exchange=model_config.exchange,
                         routing_key='{}.{}'.format('merged',
                                                    getattr(into_this, model_config.natural_key)))
