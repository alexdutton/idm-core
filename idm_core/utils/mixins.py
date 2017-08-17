from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View
from django_fsm import has_transition_perm
from rest_framework.exceptions import PermissionDenied


class FSMTransitionViewMixin(View):
    available_transitions = set()

    def get_transition_kwargs(self, name):
        return {}

    def post(self, request, **kwargs):
        if 'transition' in request.POST:
            with transaction.atomic():
                self.object = self.get_object(self.get_queryset().select_for_update())
                if request.POST.get('transition') in self.available_transitions:
                    transition = getattr(self.object, request.POST['transition'])
                    if not has_transition_perm(transition, request.user):
                        raise PermissionDenied
                    transition_kwargs = self.get_transition_kwargs(request.POST['transition']) or {}
                    transition(**transition_kwargs)
                    self.object.save()
                    return redirect(request.POST.get('next') or self.request.build_absolute_uri())
                else:
                    return HttpResponseBadRequest()
        else:
            try:
                method = super().post
            except AttributeError:
                return HttpResponseBadRequest()
            else:
                return method(request, **kwargs)
