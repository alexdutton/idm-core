from django.contrib import admin
import django.db.models
from django.forms import widgets

from . import models

class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

admin.site.register(models.Person, PersonAdmin)
