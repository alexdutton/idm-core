import dateutil.parser
from django.utils import timezone
from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from ..views import PersonSubViewMixin
from . import models, serializers


class RelationshipViewSet(PersonSubViewMixin,
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


class UnitViewSet(PersonSubViewMixin, viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class AffiliationTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AffiliationType.objects.all()
    serializer_class = serializers.AffiliationTypeSerializer


class RoleTypeViewSet(viewsets.ModelViewSet):
    queryset = models.RoleType.objects.all()
    serializer_class = serializers.RoleTypeSerializer
