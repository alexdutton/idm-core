from rest_framework import viewsets

from . import models, serializers


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
