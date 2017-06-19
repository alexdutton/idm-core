from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from idm_core.person.models import Person

__all__ = ['IndexView']


class IndexView(LoginRequiredMixin, DetailView):
    template_name = 'index.html'
    model = Person

    def get_object(self):
        return self.request.user.identity

    def get_context_data(self, object):
        return {
            'object': object,
        }
