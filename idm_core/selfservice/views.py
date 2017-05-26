from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from idm_core.attestation.models import SourceDocument


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'selfservice/index.html'

    def get_context_data(self, **kwargs):
        return {
            'identity': self.request.user.identity,
        }


class SourceDocumentListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        self.identity = self.user.identity
        return SourceDocument.objects.filter(identity=self.identity)
