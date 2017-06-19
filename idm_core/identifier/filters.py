from rest_framework.filters import BaseFilterBackend

from idm_core.identifier.models import Identifier


class IdentifierFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        print("RAA")
        print(request.GET)
        if 'identifierType' in request.GET:
            print("Here")
            identifiers = Identifier.objects.filter(type_id=request.GET['identifierType'])
            if 'identifierValue' in request.GET:
                identifiers = identifiers.filter(value__in=request.GET.getlist('identifierValue'))
            queryset = queryset.filter(identifiers=identifiers)
        return queryset
