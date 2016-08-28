from rest_framework.viewsets import ModelViewSet

from oxidentity.models import Person
from oxidentity.serializers import PersonSerializer


class SubPersonMixin(object):
    """
    A mixin to restrict the queryset to the person specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'person_pk' in self.kwargs:
            queryset = queryset.filter(person__pk=self.kwargs['person_pk'])
        return queryset


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.select_related('gender').all()
    serializer_class = PersonSerializer
    #lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        return super(PersonViewSet, self).create(request, *args, **kwargs)