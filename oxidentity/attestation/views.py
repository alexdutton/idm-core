from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class SourceDocumentViewSet(ModelViewSet):
    queryset = models.SourceDocument.objects.all()
    serializer_class = serializers.SourceDocumentSerializer


class AttestationViewSet(ModelViewSet):
    queryset = models.Attestation.objects.all()
    serializer_class = serializers.AttestationSerializer

