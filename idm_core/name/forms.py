import collections
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
    components = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, instance=None, initial=None, **kwargs):
        if instance is not None:
            components_by_type = collections.defaultdict(list)
            for component in instance.components:
                if isinstance(component, dict):
                    components_by_type[component['type']].append(component['value'])
            initial = {
                'title': (components_by_type['title'] + [''])[0],
                'given': (components_by_type['given'] + [''])[0],
                'middle_1': (components_by_type['middle'] + [''])[0],
                'middle_2': (components_by_type['middle'] + ['', ''])[1],
                'middle_3': (components_by_type['middle'] + ['', '', ''])[2],
                'family': (components_by_type['family'] + [''])[0],
                'suffix': (components_by_type['suffix'] + [''])[0],
                **(initial or {})
            }
        super().__init__(*args, instance=instance, initial=initial, **kwargs)

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