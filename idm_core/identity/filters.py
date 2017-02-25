from rest_framework.filters import BaseFilterBackend

from idm_core.organization.models import Organization
from idm_core.relationship.models import Affiliation
from . import models


class IdentityPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_anonymous:
            return queryset.none()
        print(request.user, type(request.user))
        identity_permissions = models.IdentityPermission.objects.filter(identity=request.user.identity)
        organizations = Organization.objects.filter(identity_permissions=identity_permissions)
        affiliations = Affiliation.objects.filter(organization=organizations, state__in=('requested', 'forthcoming', 'active', 'suspended'))
        queryset = queryset.objects.filter(affiliation=affiliations)
        return queryset