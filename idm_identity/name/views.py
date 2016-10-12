from rest_framework.viewsets import ModelViewSet

from idm_identity.name.models import Name
from idm_identity.name.serializers import NameSerializer


class NameViewSet(ModelViewSet):
    queryset = Name.objects.all()
    serializer_class = NameSerializer