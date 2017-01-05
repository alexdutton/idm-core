from django.apps import apps, AppConfig


class OrgRelationshipConfig(AppConfig):
    name = 'idm_core.relationship'
    verbose_name = 'Roles and affiliations'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.AffiliationSerializer, 'exchange': 'affiliation'},
            {'serializer': serializers.RoleSerializer, 'exchange': 'role'},
            {'serializer': serializers.AffiliationTypeSerializer, 'exchange': 'reference'},
            {'serializer': serializers.RoleTypeSerializer, 'exchange': 'reference'},
        ])
