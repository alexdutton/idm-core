from django.contrib import admin


class RelationshipAdmin(admin.ModelAdmin):
    list_filter = ('state', 'organization', 'type', 'suspended')
    readonly_fields = ('state', 'suspended')
    list_display = ('pk', 'identity', 'organization', 'type', 'state', 'suspended')
