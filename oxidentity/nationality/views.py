from rest_framework import viewsets

from oxidentity.views import SubPersonMixin
from . import models, serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()


class NationalityViewSet(SubPersonMixin, viewsets.ModelViewSet):
    serializer_class = serializers.NationalitySerializer
    queryset = models.Nationality.objects.all()
