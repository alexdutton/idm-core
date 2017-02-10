from django.apps import apps, AppConfig


class IdentityConfig(AppConfig):
    name = 'idm_core.identity'
    verbose_name = 'Identities'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_broker').register_notifications([
        ])
