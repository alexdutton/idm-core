from rest_framework import viewsets

from idm_core.views import PersonSubViewMixin
from . import models, serializers


class IdentifierTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.IdentifierTypeSerializer
    queryset = models.IdentifierType.objects.all()


class IdentifierViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.IdentifierSerializer
    queryset = models.Identifier.objects.all()
