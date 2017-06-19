from django.apps import apps, AppConfig


class OrganizationConfig(AppConfig):
    name = 'idm_core.organization'
    verbose_name = 'Organisations'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.OrganizationSerializer, 'exchange': 'reference'},
            {'serializer': serializers.AffiliationSerializer, 'exchange': 'affiliation'},
            {'serializer': serializers.RoleSerializer, 'exchange': 'role'},
            {'serializer': serializers.AffiliationTypeSerializer, 'exchange': 'reference'},
            {'serializer': serializers.RoleTypeSerializer, 'exchange': 'reference'},
        ])
