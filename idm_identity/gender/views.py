from rest_framework.viewsets import ModelViewSet

from idm_identity.gender.models import Gender
from idm_identity.gender.serializers import GenderSerializer


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer