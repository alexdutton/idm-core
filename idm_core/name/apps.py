import collections
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
        from idm_core.name.models import Name
        single_names = target.names.filter(state='accepted',
                                           context__only_one_accepted=True).values_list('context_id', flat=True)
        existing_multiple_names = collections.defaultdict(set)
        for name in target.names.filter(state='accepted',
                                           context__only_one_accepted=False):
            existing_multiple_names[name.context_id].add(name.marked_up)

        for name in Name.objects.filter(state='accepted').exclude(context_id__in=single_names):
            if name.marked_up not in existing_multiple_names[name.context_id]:
                name.pk = None
                name.identity = target
                name.save()
