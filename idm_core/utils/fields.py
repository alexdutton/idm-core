from django.db import models
from django_fsm import FSMFieldMixin


class FSMBooleanField(FSMFieldMixin, models.BooleanField):
    """
    Same as FSMField, but stores the state value in a BooleanField.
    """
    pass
