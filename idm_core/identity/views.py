from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from . import models, serializers


class IdentitySubViewMixin(object):
    """
    A mixin to restrict the queryset to the identity specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'person_pk' in self.kwargs:
            queryset = queryset.filter(person_id=self.kwargs['person_pk'])
        return queryset


class IdentityViewSet(get_viewset_transition_action_mixin(models.Identity, 'state'),
                      ReadOnlyModelViewSet):
    queryset = models.Identity.objects.all()
    serializer_class = serializers.IdentitySerializer

    lookup_value_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


class PersonViewSet(ModelViewSet):
    queryset = models.Identity.people.all()
    serializer_class = serializers.PersonSerializer
