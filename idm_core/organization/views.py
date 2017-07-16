from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView

from idm_core.organization.models import Organization
from . import models, forms, filters


class OrganizationListView(LoginRequiredMixin, ListView):
    queryset = models.Organization.objects.order_by('label')
    paginate_by = 100


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = models.Organization

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if not self.request.user.has_perm('organization.manage_organization', object):
            raise PermissionDenied
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'organization': self.object,
            'organization_pk': str(self.object.pk),
        })
        return context


class OrganzationSubView(View):
    organization_permission = None

    def dispatch(self, request, *args, **kwargs):
        self.organization = get_object_or_404(Organization, pk=self.kwargs['organization_pk'])
        if self.organization_permission and not self.request.user.has_perm(self.organization_permission, self.organization):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(organization=self.organization)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'organization': self.organization,
                        'organization_pk': str(self.organization.pk)})
        return context


class AffiliationListView(LoginRequiredMixin, OrganzationSubView, FilterView, ListView):
    model = models.Affiliation
    organization_permission = 'organization.view_affiliations'
    filterset_class = filters.AffiliationFilter
    paginate_by = 100


class AffiliationCreateView(LoginRequiredMixin, OrganzationSubView, CreateView):
    model = models.Affiliation
    organization_permission = 'organization.offer_affiliations'
    form_class = forms.AffiliationForm

    def form_valid(self, form):
        form.instance.organization = self.organization
        return super().form_valid(form)


class AffiliationUpdateView(LoginRequiredMixin, OrganzationSubView, UpdateView):
    model = models.Affiliation
    form_class = forms.AffiliationForm
    organization_permission = 'organization.manage_affiliations'
    form_class = forms.AffiliationForm
