from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Identifiable(models.Model):
    identifiers = GenericRelation('identifier.Identifier', 'identity_id', 'identity_content_type')

    class Meta:
        abstract = True


class IdentifierFilterViewSetMixin(object):
    def get_queryset(self):
        from .models import Identifier
        queryset = super().get_queryset()
        if 'identifierType' in self.request.GET and 'identifier' in self.request.GET:
            identifier_type = self.request.GET['identifierType']
            identifiers = self.request.GET.getlist('identifier')
            identity_ids = Identifier.objects.filter(type_id=identifier_type,
                                                     value__in=identifiers).values_list('identity_id',
                                                                                        flat=True)
            queryset = queryset.filter(id__in=identity_ids)
        return queryset
