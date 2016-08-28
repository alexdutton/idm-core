from rest_framework.viewsets import ModelViewSet

from oxidentity.name.models import Name
from oxidentity.name.serializers import NameSerializer


class NameViewSet(ModelViewSet):
    queryset = Name.objects.all()
    serializer_class = NameSerializer