from django import forms

from . import models


class AffiliationForm(forms.ModelForm):
    class Meta:
        model = models.Affiliation
        fields = (
            'identity', 'type', 'course', 'start_date', 'end_date', 'effective_start_date', 'effective_end_date', 'review_date',
            'comment',
        )
