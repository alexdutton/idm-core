from django.apps import apps, AppConfig


class PersonConfig(AppConfig):
    name = 'idm_core.person'
    verbose_name = 'people'

    def ready(self):
        from . import serializers
        apps.get_app_config('idm_broker').register_notifications([
            {'serializer': serializers.PersonSerializer, 'exchange': 'person'},
        ])
