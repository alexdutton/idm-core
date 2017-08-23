from django.apps import apps, AppConfig

from idm_core.identity.signals import pre_merge


class NationalityConfig(AppConfig):
    name = 'idm_core.nationality'
    verbose_name = 'Countries and nationality'

    def ready(self):
        from . import serializers
        from idm_core.person.models import Person
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.CountrySerializer, 'exchange': 'reference'},
            {'serializer': serializers.NationalitySerializer, 'exchange': 'nationality'},
        ])
        pre_merge.connect(self.on_person_merge, sender=Person)

    def on_person_merge(self, target, others, other_ids, **kwargs):
        from . import models
        nationalities = target.nationalities.all()
        for nationality in models.Nationality.objects.filter(identity_id__in=other_ids):
            if nationality.country in nationalities:
                nationality.attestations.all().delete()
                nationality.delete()
            else:
                nationality.identity = target
                nationality.save()
