from django.apps import apps, AppConfig


class ApplicationConfig(AppConfig):
    name = 'idm_core.application'

    def ready(self):
        from . import serializers
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.ApplicationSerializer, 'exchange': 'application'},
        ])
