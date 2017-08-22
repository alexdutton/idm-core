from django.contrib import admin

from . import models


class ApplicationAdmin(admin.ModelAdmin):
    fields = ('label', 'manageable_content_types')

admin.site.register(models.Application, ApplicationAdmin)
