from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from . import models


class OrganizationIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')
    state = indexes.FacetCharField(model_attr='state')
    tags = indexes.FacetMultiValueField()

    def prepare_tags(self, my_model):
        return [tag.id for tag in my_model.tags.all()]

    def get_model(self):
        return models.Organization

    # def index_queryset(self):
    #     return models.Organization.objects.filter(state=)