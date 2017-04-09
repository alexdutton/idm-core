from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from idm_core.application.serializers import ApplicationSerializer


class ManageableModel(models.Model):
    managed_by = models.ForeignKey('application.Application', null=True, blank=True, default=None)
    unmanaged_fields = ArrayField(models.CharField(max_length=64), default=[])
    manage_url = models.URLField(blank=True)
    upstream_id = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        abstract = True


class ManageableModelSerializer(serializers.ModelSerializer):
    managed_by = ApplicationSerializer(read_only=True)
    managed = serializers.BooleanField(required=False, write_only=True)
    unmanaged_fields = serializers.ListField(serializers.CharField(), required=False)
    manage_url = serializers.URLField(required=False)
    upstream_id = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = kwargs.get('partial', True)
        return super().__init__(*args, **kwargs)

    def validate(self, attrs):
        from .models import Application
        identity = self.context['request'].user.identity

        # Check whether the user can
        if 'managed' in attrs:
            managed = attrs.pop('managed')
            if not isinstance(identity, Application):
                raise PermissionDenied("Only applications can edit 'managed'")
            manageable_models = [ct.model_class() for ct in identity.manageable_content_types.all()]
            if self.Meta.model not in manageable_models:
                raise PermissionDenied("Application isn't allowed to manage this type of resource")
            if self.instance and self.instance.managed_by_id not in (identity.id, None):
                raise PermissionDenied("This resource is already managed by another application")
            if managed is True:
                attrs['managed_by'] = identity
            elif managed is False:
                attrs['managed_by'] = None
        else:
            managed = bool(self.instance.managed_by_id) if self.instance else False

        if self.instance and managed and self.instance.managed_by_id not in (None, identity.id):
                for field_name, field in self.get_fields().items():
                    if getattr(self.instance, field.source) != attrs.get(field_name) and field:
                        pass

        return super().validate(attrs)

    class Meta:
        fields = ('managed_by', 'managed', 'unmanaged_fields', 'manage_url', 'upstream_id')
