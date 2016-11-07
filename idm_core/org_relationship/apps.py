from django.apps import apps, AppConfig


class OrgRelationshipConfig(AppConfig):
    name = 'idm_core.org_relationship'
    verbose_name = 'Roles and affiliations'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('notification').register_many([
            (models.Affiliation, serializers.AffiliationSerializer, 'affiliation'),
            (models.Role, serializers.RoleSerializer, 'role'),
            (models.AffiliationType, serializers.AffiliationTypeSerializer, 'reference'),
            (models.RoleType, serializers.RoleTypeSerializer, 'reference'),
        ])
