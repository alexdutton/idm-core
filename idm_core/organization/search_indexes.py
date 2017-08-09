from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from . import models


class OrganizationIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content')

    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')
    state = indexes.FacetCharField(model_attr='state')
    tags = indexes.FacetMultiValueField(model_attr='tags')

    def get_model(self):
        return models.Organization
