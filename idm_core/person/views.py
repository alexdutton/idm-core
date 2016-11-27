from rest_framework.viewsets import ModelViewSet

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from . import models, serializers


class PersonSubViewMixin(object):
    """
    A mixin to restrict the queryset to the person specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'person_pk' in self.kwargs:
            queryset = queryset.filter(person_id=self.kwargs['person_pk'])
        return queryset


class PersonViewSet(get_viewset_transition_action_mixin(models.Person, 'state'),
                    ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

    lookup_value_regex = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def create(self, request, *args, **kwargs):
        return super(PersonViewSet, self).create(request, *args, **kwargs)
