from rest_framework import viewsets

from idm_core.views import PersonSubViewMixin
from . import models, serializers


class EmailViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()


class TelephoneViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TelephoneSerializer
    queryset = models.Telephone.objects.all()


class AddressViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
