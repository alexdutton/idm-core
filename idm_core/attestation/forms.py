from django import forms
from django.contrib.contenttypes.models import ContentType

from . import models


class SourceDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = models.SourceDocument
        fields = ('type', 'label', 'document')


class SourceDocumentAttestationForm(forms.Form):
    def __init__(self, *args, attestables=(), **kwargs):
        super().__init__(*args, **kwargs)
        for attestable in attestables:
            field = forms.BooleanField(label=str(attestable), required=False)
            field.attestable = attestable
            self.fields['attests-{}-{}'.format(ContentType.objects.get_for_model(attestable).pk,
                                               attestable.pk)] = field
