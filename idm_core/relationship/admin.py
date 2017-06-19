from django.contrib import admin

from . import models


class RelationshipAdmin(admin.ModelAdmin):
    list_filter = ('state', 'organization', 'type', 'suspended')
    readonly_fields = ('state', 'suspended')
    list_display = ('pk', 'identity', 'organization', 'type', 'state', 'suspended')
