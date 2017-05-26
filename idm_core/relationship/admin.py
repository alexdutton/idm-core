from django.contrib import admin

from . import models


class RelationshipAdmin(admin.ModelAdmin):
    list_filter = ('state', 'organization', 'type', 'suspended')
    readonly_fields = ('state', 'suspended')
    list_display = ('pk', 'identity', 'organization', 'type', 'state', 'suspended')


@admin.register(models.Affiliation)
class AffiliationAdmin(RelationshipAdmin):
    pass


@admin.register(models.Role)
class RoleAdmin(RelationshipAdmin):
    pass

@admin.register(models.OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'organization', 'role_label', 'role_type')
    list_filter = ('organization', 'role_type')