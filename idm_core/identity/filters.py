import django_filters
from rest_framework.filters import BaseFilterBackend

from idm_core.organization.models import Organization, Affiliation
from . import models


class IdentityPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_anonymous:
            return queryset.none()
        if not request.user.identity_id:
            return queryset.none()
        identity_permissions = models.IdentityPermission.objects.filter(identity_id=request.user.identity_id)
        organizations = Organization.objects.filter(identity_permissions=identity_permissions)
        affiliations = Affiliation.objects.filter(organization=organizations, state__in=('requested', 'forthcoming', 'active', 'suspended'))
        queryset = queryset.filter(affiliation=affiliations)
        return queryset


class IdentityStateFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset


class IdentityFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(choices=models.IDENTITY_STATE_CHOICES,
                                        label='State')
