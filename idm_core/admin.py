from django.contrib import admin
import django.db.models
from django.contrib.admin.options import InlineModelAdmin
from django.forms import widgets
from reversion.admin import VersionAdmin

from idm_core.name.models import Name
from . import models


class NameInlineModelAdmin(InlineModelAdmin):
    model = Name
    exclude = ('attestations',)


@admin.register(models.Identity)
class PersonAdmin(VersionAdmin):
    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

    readonly_fields = ('state',)
    #inlines = (NameInlineModelAdmin,)