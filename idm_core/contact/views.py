from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from idm_core.identity.views import IdentitySubViewMixin
from . import models, serializers


class EmailViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class TelephoneViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TelephoneSerializer
    queryset = models.Telephone.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class AddressViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class OnlineAccountViewSet(IdentitySubViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.OnlineAccountSerializer
    queryset = models.OnlineAccount.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
