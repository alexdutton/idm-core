from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    fields = ('identity_content_type', 'identity_id', 'principal_name')
    list_display = ('id', 'identity_content_type', 'identity_id')
    list_filter = ('identity_content_type',)

admin.site.register(models.User, UserAdmin)