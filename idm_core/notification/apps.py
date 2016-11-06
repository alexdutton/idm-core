from django.apps import AppConfig
from django.db.models.signals import pre_delete, post_save


class NotificationConfig(AppConfig):
    name = 'idm_core.notification'

    def ready(self):
        from . import messaging

        messaging.init()
        post_save.connect(messaging.instance_changed)
        pre_delete.connect(messaging.instance_deleted)
