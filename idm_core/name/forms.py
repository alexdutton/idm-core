from django import forms

from . import models
from .utils import intersperse


class SimpleNameForm(forms.ModelForm):
    title = forms.CharField(required=False)
    given = forms.CharField()
    middle_1 = forms.CharField(required=False)
    middle_2 = forms.CharField(required=False)
    middle_3 = forms.CharField(required=False)
    family = forms.CharField()
    suffix = forms.CharField(required=False)
    components = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        component_mapping = [('title', 'title'),
                             ('given', 'given'),
                             ('middle_1', 'middle'),
                             ('middle_2', 'middle'),
                             ('middle_3', 'middle'),
                             ('family', 'family'),
                             ('suffix', 'suffix')]
        components = [{'type': ctype, 'value': self.cleaned_data[field]}
                      for field, ctype in component_mapping
                      if self.cleaned_data.get(field)]
        for field, _ in component_mapping:
            self.cleaned_data.pop(field, None)
        self.cleaned_data['components'] = list(intersperse(components, ' '))
        return self.cleaned_data

    class Meta:
        model = models.Name
        fields = ('components',)