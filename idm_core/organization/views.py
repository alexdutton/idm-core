from rest_framework import viewsets

from idm_core.identity.views import IdentityViewSet
from . import models, serializers


class OrganizationViewSet(IdentityViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
