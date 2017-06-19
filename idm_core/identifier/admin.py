from django.contrib import admin

from . import models


class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'identity_content_type', 'identity_id')
    list_filter = ('type', 'identity_content_type')


admin.site.register(models.Identifier, IdentifierAdmin)
