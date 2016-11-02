from django.contrib import admin

from . import models


@admin.register(models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_filter = ('state', 'organization', 'suspended')


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_filter = ('state', 'organization', 'suspended')

