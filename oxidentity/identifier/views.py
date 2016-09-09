from rest_framework import viewsets

from oxidentity.views import SubPersonMixin
from . import models, serializers


class IdentifierTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.IdentifierTypeSerializer
    queryset = models.IdentifierType.objects.all()


class IdentifierViewSet(SubPersonMixin, viewsets.ModelViewSet):
    serializer_class = serializers.IdentifierSerializer
    queryset = models.Identifier.objects.all()
