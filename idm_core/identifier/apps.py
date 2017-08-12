from django.apps import apps, AppConfig

from idm_core.identity.signals import pre_merge


class IdentifierConfig(AppConfig):
    name = 'idm_core.identifier'
    verbose_name = 'identifier'

    def ready(self):
        from . import models
        from idm_core.person.models import Person
        apps.get_app_config('idm_broker').register_related_notification(model=models.Identifier,
                                                                        accessor=lambda name: name.identity)
        pre_merge.connect(self.on_person_merge, sender=Person)

    def on_person_merge(self, target, others, other_ids, **kwargs):
        from . import models

        for identifier in models.Identifier.objects.filter(identity_id__in=other_ids):
            identifier.identity = target
            identifier.save()
