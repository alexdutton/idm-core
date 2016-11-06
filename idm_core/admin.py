from django.contrib import admin
import django.db.models
from django.contrib.admin.options import InlineModelAdmin, TabularInline
from django.forms import widgets
from reversion.admin import VersionAdmin

from idm_core.name.models import Name
from idm_core.org_relationship.models import Affiliation
from . import models


class NameInlineModelAdmin(TabularInline):
    model = Name
    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }
    fields = ('components', 'contexts', 'active', 'space_delimited')


class AffiliationInlineModelAdmin(TabularInline):
    model = Affiliation
    fields = ('organization', 'type', 'state', 'start_date', 'end_date', 'effective_end_date')
    readonly_fields = ('state',)


@admin.register(models.Person)
class PersonAdmin(VersionAdmin):
    formfield_overrides = {
        django.db.models.TextField: {'widget': widgets.TextInput},
    }

    list_display = ('id', 'get_first_name', 'get_last_name', 'primary_email', 'primary_username', 'state')
    list_filter = ('state',)

    def get_first_name(self, obj):
        return obj.primary_name.first if obj.primary_name_id else ''
    get_first_name.short_description = 'First name'
    get_first_name.admin_order_field = 'primary_name__first'

    def get_last_name(self, obj):
        return obj.primary_name.last if obj.primary_name_id else ''
    get_last_name.short_description = 'Last name'
    get_last_name.admin_order_field = 'primary_name__last'

    readonly_fields = ('state', 'primary_email', 'primary_username', 'primary_name', 'merged_into')
    inlines = (NameInlineModelAdmin, AffiliationInlineModelAdmin)
