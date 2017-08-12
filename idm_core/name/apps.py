from django.apps import apps, AppConfig

from idm_core.identity.signals import pre_merge


class NameConfig(AppConfig):
    name = 'idm_core.name'
    verbose_name = 'name'

    def ready(self):
        from . import models
        from idm_core.person.models import Person
        apps.get_app_config('idm_broker').register_related_notification(model=models.Name,
                                                                        accessor=lambda name: name.identity)
        pre_merge.connect(self.on_person_merge, sender=Person)

    def on_person_merge(self, target, others, other_ids, **kwargs):
        names = set(name.marked_up for name in target.names.all())
        deleted_names = set()
        from idm_core.name.models import Name
        for name in Name.objects.filter(identity_id__in=other_ids):
            if name.marked_up in names:
                deleted_names.add(name.pk)
                name.attestations.all().delete()
                name.delete()
            else:
                name.pk = None
                name.identity = target
                name.save()

        for other in others:
            if other.primary_name_id in deleted_names or other.primary_name_id == other.primary_name_id:
                other.primary_name_id = None
