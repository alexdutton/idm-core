from rest_framework.viewsets import ModelViewSet

from idm_identity.models import Identity
from idm_identity.serializers import IdentitySerializer


class IdentitySubViewMixin(object):
    """
    A mixin to restrict the queryset to the identity specified in the URL.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'identity_pk' in self.kwargs:
            queryset = queryset.filter(identity_pk=self.kwargs['identity_pk'])
        return queryset


class IdentityViewSet(ModelViewSet):
    queryset = Identity.objects.select_related('gender').all()
    serializer_class = IdentitySerializer
    #lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        return super(IdentityViewSet, self).create(request, *args, **kwargs)