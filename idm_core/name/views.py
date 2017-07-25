from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView

from idm_core.attestation.models import SourceDocument
from idm_core.name.forms import SimpleNameForm
from idm_core.name.models import Name
from idm_core.person.models import Person
from idm_core.selfservice.views.base import SameIdentityMixin

__all__ = ['NameListView', 'NameDetailView']

class NameListView(LoginRequiredMixin, SameIdentityMixin, ListView):
    model = Name


class NameDetailView(LoginRequiredMixin, SameIdentityMixin, UpdateView):
    model = Name
    form_class = SimpleNameForm
#    template_name = 'name/name_form.html'


class SourceDocumentListView(LoginRequiredMixin, SameIdentityMixin, ListView):
    model = SourceDocument
