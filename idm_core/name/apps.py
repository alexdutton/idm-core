from django.apps import apps, AppConfig


class NameConfig(AppConfig):
    name = 'idm_core.name'
    verbose_name = 'name'

    def ready(self):
        from . import models
        apps.get_app_config('idm_broker').register_related_notification(model=models.Name,
                                                                        accessor=lambda name: name.identity)
