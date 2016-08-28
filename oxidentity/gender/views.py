from rest_framework.viewsets import ModelViewSet

from oxidentity.gender.models import Gender
from oxidentity.gender.serializers import GenderSerializer


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer