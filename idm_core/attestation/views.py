import os
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory, formset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from formtools.wizard.views import SessionWizardView

from idm_core.attestation.mixins import Attestable
from idm_core.identity.models import Identity

from . import forms, models


class SourceDocumentView(View):
    model = models.SourceDocument
    identity = None

    def dispatch(self, request, *args, **kwargs):
        if 'identity_type' in self.kwargs:
            self.identity = Identity.objects.get(id=self.kwargs['identity_id']).identity
            if self.kwargs['identity_type'] != self.identity.type_slug:
                raise Http404
        elif self.request.user.identity:
            self.identity = self.request.user.identity
        else:
            raise Http404
        self.identity_self = 'identity_type' not in self.kwargs

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(identity_id=self.identity.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'identity': self.identity,
            'self': self.identity_self,
        })
        return context


class SourceDocumentListView(SourceDocumentView, ListView):
    pass


class SourceDocumentWizardView(SourceDocumentView, SessionWizardView):
    form_list = (
        ('upload', forms.SourceDocumentUploadForm),
        ('attestation', forms.SourceDocumentAttestationForm)
    )

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'source-wizard-tmp'))
    template_name = 'attestation/sourcedocument_wizard.html'

    def get_attestables(self):
        attestables = []
        for model in apps.get_models():
            if issubclass(model, Attestable):
                attestables.extend(model.objects.filter(identity_id=self.identity.id))
        return attestables

    def get_form_instance(self, step):
        print(step)
        if step == 'upload':
            return models.SourceDocument(identity=self.identity,
                                         validated_by=self.request.user)

    def get_form_kwargs(self, step):
        if step == 'attestation':
            return {'attestables': self.get_attestables()}
        else:
            return {}

    def done(self, form_list, form_dict, **kwargs):
        form_dict['upload'].save()

        if 'identity_type' in self.kwargs:
            return redirect(reverse('attestation:source-document-list', kwargs=self.kwargs))
        else:
            return redirect(reverse('attestation:source-document-list-self', kwargs=self.kwargs))