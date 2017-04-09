from idm_core.identity.views import IdentityViewSet
from . import models, serializers


class ApplicationViewSet(IdentityViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
