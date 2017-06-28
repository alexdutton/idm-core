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

    @detail_route(methods=['post'])
    def activate(self, request, pk=None):
        object = self.get_object()
        object.identity.activate()
        return Response(status=204)