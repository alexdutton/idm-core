from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import ForeignKey
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from idm_core.attestation.mixins import Attestable
from idm_core.identity.views import IdentitySubViewMixin
from . import models, serializers


class SourceDocumentViewSet(ModelViewSet):
    queryset = models.SourceDocument.objects.all()
    serializer_class = serializers.SourceDocumentSerializer


class AttestationViewSet(ModelViewSet):
    queryset = models.Attestation.objects.all()
    serializer_class = serializers.AttestationSerializer


class AttestableViewSet(IdentitySubViewMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    serializer_class = serializers.AttestableSerializer

    def get_queryset(self):
        attestables = []
        for model in apps.get_models():
            if issubclass(model, Attestable):
                attestables.extend(model.objects.filter(identity_id=self.kwargs['identity_pk']))
        return attestables
