from rest_framework.serializers import HyperlinkedModelSerializer

from idm_core.person.serializers import TypeMixin

from . import models


class OrganizationSerializer(TypeMixin, HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization
        fields = ('id', 'label', 'tags')
