from rest_framework import viewsets

from idm_identity.views import IdentitySubViewMixin
from . import models, serializers


class EmailViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()


class TelephoneViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TelephoneSerializer
    queryset = models.Telephone.objects.all()


class AddressViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
