from django.contrib import admin
import django.db.models
from django.forms import widgets

from . import models


class NameAdmin(admin.ModelAdmin):

    list_display = ('plain', 'familiar', 'sort', 'first', 'last')
    list_filter = ('context',)

    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

admin.site.register(models.Name, NameAdmin)
