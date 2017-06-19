from rest_framework.filters import BaseFilterBackend

from idm_core.relationship import models


class AffiliationFilterBackend(BaseFilterBackend):
    def get_queryset(self, request, queryset, view):
        if 'affiliationOrganization' in request.GET:
            organization_ids = request.GET.getlist('affiliationOrganization')
            states = request.GET.getlist('affiliationState') or ('active',)
            affiliations = models.Affiliation.objects.filter(organization_id__in=organization_ids,
                                                             state__in=states)
            if 'affiliationType' in self.request.GET:
                affiliations = affiliations.filter(type_id__in=request.GET.getlist('affiliationType'))
            queryset = queryset.filter(affiliation=affiliations)
        return queryset



class RoleFilterBackend(BaseFilterBackend):
    def get_queryset(self, request, queryset, view):
        if 'roleOrganization' in request.GET:
            organization_ids = request.GET.getlist('affiliationOrganization')
            states = request.GET.getlist('affiliationState') or ('active',)
            affiliations = models.Affiliation.objects.filter(organization_id__in=organization_ids,
                                                             state__in=states)
            if 'affiliationType' in self.request.GET:
                affiliations = affiliations.filter(type_id__in=request.GET.getlist('affiliationType'))
            queryset = queryset.filter(affiliation=affiliations)
        return queryset
