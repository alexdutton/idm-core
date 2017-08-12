from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete

from idm_core.identity.signals import pre_merge


class AttestationConfig(AppConfig):
    name = 'idm_core.attestation'

    def ready(self):
        from idm_core.person.models import Person
        from . import models
        post_save.connect(self.update_attested_by, sender=models.Attestation)
        pre_delete.connect(self.update_attested_by, sender=models.Attestation)
        pre_merge.connect(self.on_person_merge, sender=Person)

    def update_attested_by(self, sender, instance, created=None, **kwargs):
        """"""
        attested = instance.attests
        attested.attested_by = sorted(set(a.source_document.type
                                          for a in attested.attestations.select_related('source_document').all()))
        instance.attests.save()

    def on_person_merge(self, target, other_ids, **kwargs):
        from . import models
        for source_document in models.SourceDocument.objects.filter(identity_id__in=other_ids):
            source_document.person = target
            source_document.save()
