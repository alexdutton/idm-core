from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin

from . import models, serializers

class IdentitySubViewMixin(object):
    """
    A mixin to restrict the queryset to the identity specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'identity_pk' in self.kwargs:
            queryset = queryset.filter(identity_pk=self.kwargs['identity_pk'])
        return queryset


class IdentityViewSet(get_viewset_transition_action_mixin(models.Identity, 'state'),
                      ModelViewSet):
    queryset = models.Identity.objects.all()
    serializer_class = serializers.IdentitySerializer

    def create(self, request, *args, **kwargs):
        return super(IdentityViewSet, self).create(request, *args, **kwargs)
