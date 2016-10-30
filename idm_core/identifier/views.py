from rest_framework import viewsets

from idm_core.views import IdentitySubViewMixin
from . import models, serializers


class IdentifierTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.IdentifierTypeSerializer
    queryset = models.IdentifierType.objects.all()


class IdentifierViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.IdentifierSerializer
    queryset = models.Identifier.objects.all()
