import django_filters
from django import forms
from django.forms import widgets
from rest_framework.filters import BaseFilterBackend

from idm_core.identity.models import IDENTITY_STATE_CHOICES
from idm_core.relationship.models import RELATIONSHIP_STATE_CHOICES
from . import models


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


class AffiliationFilter(django_filters.FilterSet):
    state = django_filters.MultipleChoiceFilter(choices=RELATIONSHIP_STATE_CHOICES,
                                                label='Affiliation state')
    identity__state = django_filters.MultipleChoiceFilter(choices=IDENTITY_STATE_CHOICES,
                                                          label='Identity state')

    start_date = django_filters.DateFromToRangeFilter()
    end_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = models.Affiliation
        fields = ['state', 'identity__state', 'start_date', 'end_date']
