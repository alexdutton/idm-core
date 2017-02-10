from drf_fsm_transitions.viewset_mixins import get_viewset_transition_action_mixin
from idm_core.identity.views import IdentityViewSet

from . import models, serializers

class PersonViewSet(get_viewset_transition_action_mixin(models.Person, 'state'),
                      IdentityViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
