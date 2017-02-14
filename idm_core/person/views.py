from django.db.models import Q

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from idm_core.identity.views import IdentityViewSet
from idm_core.relationship.models import Affiliation

from . import models, serializers


class PersonViewSet(get_viewset_transition_action_mixin(models.Person, 'state'),
                      IdentityViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'affiliationOrganization' in self.request.GET:
            organization_ids = self.request.GET.getlist('affiliationOrganization')
            states = self.request.GET.getlist('affiliationState') or ('active',)
            affiliations = Affiliation.objects.filter(organization_id__in=organization_ids,
                                                      state__in=states)
            if 'affiliationType' in self.request.GET:
                affiliations = affiliations.filter(type_id__in=self.request.GET.getlist('affiliationType'))
            queryset = queryset.filter(affiliation=affiliations)
        return queryset
