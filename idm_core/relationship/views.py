import dateutil.parser
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from idm_core.identity.views import IdentitySubViewMixin
from . import models, serializers


class RelationshipViewSet(IdentitySubViewMixin,
                          get_viewset_transition_action_mixin(models.Affiliation, 'state'),
                          get_viewset_transition_action_mixin(models.Affiliation, 'suspended'),
                          viewsets.ModelViewSet):
    def get_suspend_kwargs(self):
        data = self.request.data
        if 'until' in data:
            try:
                until = dateutil.parser.parse(data['until'])
                if not until.tzinfo:
                    until = timezone.make_aware(until)
                return {'until': until}
            except ValueError:
                raise ValidationError({'detail': '"until" should be a datetime if specified'})
        return {}


class AffiliationViewSet(RelationshipViewSet):
    queryset = models.Affiliation.objects.all()
    serializer_class = serializers.AffiliationSerializer


class RoleViewSet(RelationshipViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class AffiliationTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AffiliationType.objects.all()
    serializer_class = serializers.AffiliationTypeSerializer


class RoleTypeViewSet(viewsets.ModelViewSet):
    queryset = models.RoleType.objects.all()
    serializer_class = serializers.RoleTypeSerializer
