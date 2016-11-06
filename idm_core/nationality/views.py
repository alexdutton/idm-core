from rest_framework import viewsets

from idm_core.person.views import PersonSubViewMixin
from . import models, serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()


class NationalityViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.NationalitySerializer
    queryset = models.Nationality.objects.all()
