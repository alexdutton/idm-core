from django.contrib import admin
import django.db.models
from django.forms import widgets

from . import models


class NameAdmin(admin.ModelAdmin):

    list_display = ('plain', 'familiar', 'sort', 'first', 'last', 'context')
    list_filter = ('context',)
    readonly_fields = ('identity', 'attested_by')

    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

admin.site.register(models.Name, NameAdmin)
