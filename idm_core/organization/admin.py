from django.contrib import admin

from idm_core.relationship.admin import RelationshipAdmin
from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


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