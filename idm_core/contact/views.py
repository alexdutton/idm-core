from django.http import Http404
from django.views import View
from django.views.generic import ListView, DetailView

from idm_core.identity.models import Identity
from . import models


class ContactView(View):
    identity = None

    def get_template_names(self):
        names = super().get_template_names()
        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.insert(1, "%s/contact%s.html" % (opts.app_label, self.template_name_suffix))
        return names

    def get_queryset(self):
        if 'identity_type' in self.kwargs:
            self.identity = Identity.objects.get(id=self.kwargs['identity_id']).identity
            if self.kwargs['identity_type'] != self.identity.type_slug:
                raise Http404
        elif self.request.user.identity:
            self.identity = self.request.user.identity
        else:
            raise Http404

        return super().get_queryset().filter(identity_id=self.identity.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'identity': self.identity,
            'self': 'identity_type' not in self.kwargs,
            'verbose_name_plural': self.object_list.model._meta.verbose_name_plural
        })
        return context


class ContactListView(ContactView, ListView):
    pass


class ContactDetailView(ContactView, DetailView):
    pass


class EmailListView(ContactListView):
    model = models.Email


class OnlineAccountListView(ContactListView):
    model = models.OnlineAccount


class AddressListView(ContactListView):
    model = models.Address


class TelephoneListView(ContactListView):
    model = models.Telephone
