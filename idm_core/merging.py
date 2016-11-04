import abc
from django.db import transaction, connection

from idm_core import messaging
from idm_core.nationality.models import Nationality
from idm_core.org_relationship.models import Affiliation, Role
from .models import Identity
from .attestation.models import SourceDocument
from .name.models import Name

_fields_to_copy = {'sex', 'primary_email', 'primary_username', 'date_of_birth',
                   'date_of_death'}

def merge_people(merge_these, into_this, trigger=None, reason=None):
    with transaction.atomic():
        if not isinstance(merge_these, abc.Collection):
            merge_these = (merge_these,)

        for source_document in SourceDocument.filter(identity__in=merge_these):
            source_document.identity = into_this
            source_document.save()

        names = set(name.marked_up for name in into_this.names.all())
        for name in Name.filter(identity__in=merge_these):
            if name.marked_up in names:
                name.attestations.all().delete()
                name.delete()
            else:
                name.identity = into_this
                name.save()

        nationalities = into_this.nationalities.all()
        for nationality in Nationality.objects.filter(identity__in=merge_these):
            if nationality.nationality not in nationalities:
                nationality.attestations.all().delete()
                nationality.delete()
            else:
                nationality.identity = into_this
                nationality.save()

        for affiliation in Affiliation.objects.filter(identity__in=merge_these):
            affiliation.identity = into_this
            affiliation.save()

        for role in Role.objects.filter(identity__in=merge_these):
            role.identity = into_this
            role.save()

        for identity in merge_these:
            for field_name in _fields_to_copy:
                if getattr(identity, field_name) and not getattr(into_this, field_name):
                    setattr(into_this, field_name, getattr(identity, field_name))
            identity.merge_into(into_this)
            identity.save()

        into_this.save()

    connection.on_commit(lambda : messaging.publish_merge_to_amqb(merge_these, into_this))
