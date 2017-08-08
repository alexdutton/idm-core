from django.contrib import admin

from . import models

admin.site.register(models.OnlineAccount)
admin.site.register(models.Telephone)
admin.site.register(models.Address)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('identity', 'context', 'value')

admin.site.register(models.Email, EmailAdmin)
