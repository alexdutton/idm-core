from django.apps import apps, AppConfig


class OrganizationConfig(AppConfig):
    name = 'idm_core.organization'
    verbose_name = 'Organisations'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_notification').register(serializer=serializers.OrganizationSerializer,
                                                         exchange='reference')
