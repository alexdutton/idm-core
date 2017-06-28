import collections.abc
from django.apps import apps
from django.conf import settings
from django.db import transaction, connection

from idm_core.identifier.models import Identifier
from idm_core.nationality.models import Nationality
from idm_core.organization.models import Affiliation, Role
from idm_core.attestation.models import SourceDocument
from idm_core.name.models import Name

_fields_to_copy = {'primary_email', 'primary_username', 'begin_date', 'end_date', 'date_of_birth', 'date_of_death', 'extant'}


class MergeException(Exception):
    pass


class MergeTypeDisparity(MergeException):
    pass


class MergeIntoSelfException(MergeException):
    pass


def merge(merge_these, into_this, trigger=None, reason=None):
    with transaction.atomic():
        if not isinstance(merge_these, collections.abc.Iterable):
            merge_these = (merge_these,)

        merge_ids = {i.id for i in merge_these}

        if into_this.pk in merge_ids:
            raise MergeIntoSelfException("Cannot merge identity {} into itself".format(into_this.pk))

        for identity in merge_these:
            if type(identity) != type(into_this):
                raise MergeTypeDisparity("Type of {} ({}) does not match that of {} ({})".format(
                    identity.id, type(identity).__name__, into_this.id, type(into_this).__name__
                ))

        for source_document in SourceDocument.objects.filter(identity_id__in=merge_ids):
            source_document.person = into_this
            source_document.save()

        names = set(name.marked_up for name in into_this.names.all())
        deleted_names = set()
        for name in Name.objects.filter(identity_id__in=merge_ids):
            if name.marked_up in names:
                deleted_names.add(name.pk)
                name.attestations.all().delete()
                name.delete()
            else:
                name.pk = None
                name.identity = into_this
                name.save()

        nationalities = into_this.nationalities.all()
        for nationality in Nationality.objects.filter(identity_id__in=merge_ids):
            if nationality.country in nationalities:

                nationality.attestations.all().delete()
                nationality.delete()
            else:
                nationality.identity = into_this
                nationality.save()

        for affiliation in Affiliation.objects.filter(identity_id__in=merge_ids):
            affiliation.identity = into_this
            affiliation.save()

        for role in Role.objects.filter(identity_id__in=merge_ids):
            role.identity = into_this
            role.save()

        for identifier in Identifier.objects.filter(identity_id__in=merge_ids):
            identifier.identity = into_this
            identifier.save()

        for identity in merge_these:
            for field_name in _fields_to_copy:
                if not hasattr(identity, field_name):
                    continue
                if getattr(identity, field_name) and not getattr(into_this, field_name):
                    setattr(into_this, field_name, getattr(identity, field_name))
            if identity.sex != '0' and into_this.sex == '0':
                into_this.sex = identity.sex
            if identity.primary_name_id in deleted_names or identity.primary_name_id == into_this.primary_name_id:
                identity.primary_name_id = None
            identity.merge_into(into_this)
            identity.save()

        into_this.save()

    connection.on_commit(lambda : publish_merge_to_amqp(merge_these, into_this))


def publish_merge_to_amqp(merge_these, into_this):
    broker_app_config = apps.get_app_config('idm_broker')
    with broker_app_config.broker.acquire(block=True) as conn:
        producer = conn.Producer(serializer='json')
        producer.publish({'mergedIdentities': [identity.id for identity in merge_these],
                          'targetIdentity': into_this.id},
                         exchange=settings.BROKER_PREFIX + 'identity',
                         routing_key='{}.{}.{}'.format(type(into_this).__name__,
                                                       'merged',
                                                       into_this.pk))
