from rest_framework import viewsets

from idm_identity.views import IdentitySubViewMixin
from . import models, serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()


class NationalityViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.NationalitySerializer
    queryset = models.Nationality.objects.all()
