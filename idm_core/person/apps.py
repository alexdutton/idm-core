from django.apps import apps, AppConfig


class PersonConfig(AppConfig):
    name = 'idm_core.person'
    verbose_name = 'People'

    def ready(self):
        from . import models, serializers
        apps.get_app_config('idm_notification').register(models.Person,
                                                         serializers.PlainPersonSerializer,
                                                         'person')
