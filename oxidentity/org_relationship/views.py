from rest_framework import viewsets

from oxidentity.views import SubPersonMixin
from . import models, serializers

class AffiliationViewSet(SubPersonMixin, viewsets.ModelViewSet):
    queryset = models.Affiliation.objects.all()
    serializer_class = serializers.AffiliationSerializer


class RoleViewSet(SubPersonMixin, viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class UnitViewSet(SubPersonMixin, viewsets.ModelViewSet):
    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class AffiliationTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AffiliationType.objects.all()
    serializer_class = serializers.AffiliationTypeSerializer


class RoleTypeViewSet(viewsets.ModelViewSet):
    queryset = models.RoleType.objects.all()
    serializer_class = serializers.RoleTypeSerializer
