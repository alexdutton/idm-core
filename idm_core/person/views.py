from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError

from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from idm_core.identifier.filters import IdentifierFilterBackend
from idm_core.identity.filters import IdentityPermissionFilterBackend
from idm_core.identity.views import IdentityViewSet
from idm_core.organization.models import Affiliation

from . import models, serializers


class PersonViewSet(get_viewset_transition_action_mixin(models.Person, 'state'),
                    IdentityViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    filter_backends = (
        IdentityPermissionFilterBackend,
        IdentifierFilterBackend,
    )

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

    @detail_route(methods=['post'])
    def merge(self, request, pk=None):
        with transaction.atomic():
            identity = self.get_object()
            other_ids = request.POST.getlist('id')
            others = self.get_queryset().filter(pk__in=other_ids, state__in=('established', 'active'))
            if others.count() != len(other_ids):
                missing_ids = sorted(set(other_ids) - set(others.values_list('pk', flat=True)))
                raise ValidationError("Couldn't find identities for IDs {}, or not in suitable state".format(', '.join(missing_ids)))
            identity.merge(others)
            return HttpResponse(status=204)
