from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import DetailView
from django_fsm import has_transition_perm, can_proceed, Transition
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from idm_core.identifier.mixins import IdentifierFilterViewSetMixin
from . import models, serializers


class IdentitySubViewMixin(object):
    """
    A mixin to restrict the queryset to the identity specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'identity_pk' in self.kwargs:
            queryset = queryset.filter(identity_id=self.kwargs['identity_pk'])
        return queryset


class IdentityViewSet(IdentifierFilterViewSetMixin, ModelViewSet):
    queryset = models.Identity.objects.all()
    serializer_class = serializers.IdentitySerializer

#    lookup_value_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'state' in self.request.GET:
            queryset = queryset.filter(state__in=set(self.request.GET.getlist('state')))
        return queryset

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().destroy(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def activate(self, request, pk=None):
        with transaction.atomic():
            object = self.get_object()
            object.identity.activate()
            return Response(status=204)


class IdentityDetailView(DetailView):
    available_transitions = {'activate', 'archive', 'restore', 'merge_into'}

    def get_transition_kwargs(self, name):
        if name == 'merge':
            return {'others': self.model.objects.filter(pk_in=self.request.POST.getlist('merge_into'))}
        if name == 'merge_into':
            return {'other': self.model.objects.get(pk=self.request.POST.get('merge_into'))}

    def post(self, request, **kwargs):
        with transaction.atomic():
            self.object = self.get_object(self.get_queryset().select_for_update())
            assert isinstance(self.object, models.IdentityBase)
            if request.POST.get('transition') in self.available_transitions:
                transition = getattr(self.object, request.POST['transition'])
                if not has_transition_perm(transition, request.user):
                    raise PermissionDenied
                transition_kwargs = self.get_transition_kwargs(request.POST['transition']) or {}
                transition(**transition_kwargs)
                self.object.save()
                return redirect(self.request.build_absolute_uri())
