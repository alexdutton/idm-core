from django.apps import apps, AppConfig

from idm_core.identity.signals import pre_merge


class OrganizationConfig(AppConfig):
    name = 'idm_core.organization'
    verbose_name = 'Organisations'

    def ready(self):
        from . import models, serializers
        from idm_core.person.models import Person
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.OrganizationSerializer, 'exchange': 'reference'},
            {'serializer': serializers.AffiliationSerializer, 'exchange': 'affiliation'},
            {'serializer': serializers.RoleSerializer, 'exchange': 'role'},
            {'serializer': serializers.AffiliationTypeSerializer, 'exchange': 'reference'},
            {'serializer': serializers.RoleTypeSerializer, 'exchange': 'reference'},
        ])
        apps.get_app_config('idm_broker').register_related_notification(model=models.Affiliation,
                                                                        accessor=lambda affiliation: affiliation.identity)
        pre_merge.connect(self.on_person_merge, sender=Person)
        pre_merge.connect(self.on_organization_merge, sender=models.Organization)

    def on_person_merge(self, target, others, other_ids, **kwargs):
        from . import models

        for affiliation in models.Affiliation.objects.filter(identity_id__in=other_ids):
            affiliation.identity = target
            affiliation.save()

        for role in models.Role.objects.filter(identity_id__in=other_ids):
            role.identity = target
            role.save()

    def on_organization_merge(self, target, others, other_ids, **kwargs):
        pass
