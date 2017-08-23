from django.db import transaction
from django.views.generic import DetailView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from idm_core.identifier.mixins import IdentifierFilterViewSetMixin
from idm_core.utils.mixins import FSMTransitionViewMixin
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
            identity = self.get_object()
            if isinstance(identity, models.Identity):
                identity = identity.identity
            identity.activate()
            return Response(status=204)

    @detail_route(methods=['post'])
    def merge(self, request, pk=None):
        with transaction.atomic():
            identity = self.get_object()
            if isinstance(identity, models.Identity):
                identity = identity.identity
            identity.merge(others=type(identity).objects.filter(pk__in=self.request.POST.getlist('id')))
            return Response(status=204)


class IdentityDetailView(FSMTransitionViewMixin, DetailView):
    available_transitions = {'activate', 'archive', 'restore', 'merge_into', 'merge'}

    def get_transition_kwargs(self, name):
        if name == 'merge':
            return {'others': self.model.objects.filter(pk_in=self.request.POST.getlist('id'))}
        if name == 'merge_into':
            return {'other': self.model.objects.get(pk=self.request.POST.get('merge_into'))}
