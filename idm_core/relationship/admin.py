from django.contrib import admin

from . import models


class RelationshipAdmin(admin.ModelAdmin):
    list_filter = ('state', 'target', 'type', 'suspended')
    readonly_fields = ('state', 'suspended')
    list_display = ('identity', 'target', 'type', 'state', 'suspended')


@admin.register(models.Affiliation)
class AffiliationAdmin(RelationshipAdmin):
    pass


@admin.register(models.Role)
class RoleAdmin(RelationshipAdmin):
    pass

