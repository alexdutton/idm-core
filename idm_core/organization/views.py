from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django_fsm import has_transition_perm, can_proceed

from idm_core.contact.models import Email
from idm_core.identity.views import IdentityDetailView
from idm_core.name.models import Name
from idm_core.organization.models import Organization
from idm_core.person.models import Person
from . import models, forms, filters


class OrganizationListView(LoginRequiredMixin, FilterView, ListView):
    model = models.Organization
    queryset = models.Organization.objects.order_by('label')
    filterset_class = filters.OrganizationFilter
    paginate_by = 100


class OrganizationDetailView(LoginRequiredMixin, IdentityDetailView):
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
        context.update({'identity': self.organization,
                        'organization': self.organization,
                        'organization_pk': str(self.organization.pk),
                        'base_template': 'organization/base.html'})
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(state='offered', organization=self.organization)
        return kwargs


class AffiliationInviteView(LoginRequiredMixin, OrganzationSubView, CreateView):
    model = models.Affiliation
    organization_permission = 'organization.offer_affiliations'
    form_class = forms.AffiliationInviteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(state='offered', organization=self.organization)
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            email = form.cleaned_data['email']
            try:
                # Look up person based on a validated email address
                form.instance.identity = Person.objects.get(emails=Email.objects.filter(value=email,
                                                                                        validated=True))
            except Person.DoesNotExist:
                form.instance.identity = Person.objects.create()
                Name.objects.create(identity=form.instance.identity,
                                    components=[{'type': 'given', 'value': form.cleaned_data['first_name']}, ' ',
                                                {'type': 'family', 'value': form.cleaned_data['last_name']}],
                                    context_id='presentational')
                Email.objects.create(identity=form.instance.identity,
                                     value=email,
                                     validated=False,
                                     context_id='home')
            return super().form_valid(form)


class AffiliationUpdateView(LoginRequiredMixin, OrganzationSubView, UpdateView):
    model = models.Affiliation
    form_class = forms.AffiliationForm
    organization_permission = 'organization.manage_affiliations'

    def form_valid(self, form):
        form.instance.organization = self.organization
        return super().form_valid(form)


class PersonAffiliationListView(LoginRequiredMixin, FilterView, ListView):
    model = models.Affiliation
    filterset_class = filters.AffiliationFilter
    paginate_by = 100
    template_name = 'organization/person_affiliation_list.html'

    def get_queryset(self):
        return self.request.user.identity.affiliation_set.all()


