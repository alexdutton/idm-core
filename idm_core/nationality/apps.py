from django.apps import apps, AppConfig


class NationalityConfig(AppConfig):
    name = 'idm_core.nationality'
    verbose_name = 'Countries and nationality'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_notification').register_many([
            {'serializer': serializers.CountrySerializer, 'exchange': 'reference'},
            {'serializer': serializers.NationalitySerializer, 'exchange': 'nationality'},
        ])
