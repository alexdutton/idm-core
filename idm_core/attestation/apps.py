from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete


class AttestationConfig(AppConfig):
    name = 'idm_core.attestation'

    def ready(self):
        from . import models
        post_save.connect(self.update_attested_by, sender=models.Attestation)
        pre_delete.connect(self.update_attested_by, sender=models.Attestation)

    def update_attested_by(self, sender, instance, created=None, **kwargs):
        """"""
        attested = instance.attests
        attested.attested_by = sorted(set(a.source_document.type
                                          for a in attested.attestations.select_related('source_document').all()))
        instance.attests.save()