from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from idm_core.identity.models import Identity
from idm_core.name.forms import SimpleNameForm
from idm_core.utils.mixins import FSMTransitionViewMixin
from . import models
from idm_core.selfservice.views.base import SameIdentityMixin

__all__ = ['NameListView', 'NameDetailView']


class NameView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'identity_type' in self.kwargs:
            self.is_self = False
            self.identity = Identity.objects.get(id=self.kwargs['identity_id']).identity
            if self.kwargs['identity_type'] != self.identity.type_slug:
                raise Http404
        elif self.request.user.identity:
            self.is_self = True
            self.identity = self.request.user.identity
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(identity_id=self.identity.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'identity': self.identity,
            'is_self': self.is_self,
        })
        return context


class NameListView(LoginRequiredMixin, SameIdentityMixin, ListView, NameView):
    model = models.Name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['names'] = {context: {}
                            for context in models.NameContext.objects.all()}
        for name in self.get_queryset():
            context['names'][name.context][name.state] = name
        return context


class NameDetailView(LoginRequiredMixin, FSMTransitionViewMixin, DetailView, NameView):
    model = models.Name
    available_transitions = {'accept', 'reject'}


class NameCreateView(LoginRequiredMixin, SameIdentityMixin, CreateView, NameView):
    model = models.Name
    form_class = SimpleNameForm

    def post(self, request, **kwargs):
        with transaction.atomic():
            return super().post(self, request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.model(identity_id=self.identity.id,
                              context=get_object_or_404(models.NameContext, id=self.kwargs['context']),
                              components=[])
        current = instance.get_acceptance_queryset().filter(state='accepted').first()
        if current:
            instance.components = current.components
        kwargs['instance'] = instance
        return kwargs

    def get_success_url(self):
        if self.is_self:
            return reverse('name:name-list-self')
        else:
            return reverse('name:name-list', args=(self.identity.type_slug, self.identity.id))
