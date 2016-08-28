from django.contrib import admin
import django.db.models
from django.forms import widgets

from . import models


class NameComponentInline(admin.TabularInline):
    model = models.NameComponent

    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }


class NameAdmin(admin.ModelAdmin):
    inlines = (NameComponentInline,)

    list_display = ('plain', 'familiar', 'sort', 'first', 'last')
    list_filter = ('contexts',)

    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

admin.site.register(models.Name, NameAdmin)
