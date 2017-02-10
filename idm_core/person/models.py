from django.db import models

from idm_core.identity.models import IdentityBase

# ISO/IEC 5218
SEX_CHOICES = (
    ('0', 'not known'),
    ('1', 'male'),
    ('2', 'female'),
    ('9', 'not applicable'),
)


class Person(IdentityBase):
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')
    primary_name = models.OneToOneField('name.Name', related_name='primary_name_of', null=True, blank=True, default=None)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    deceased = models.BooleanField(default=False)
