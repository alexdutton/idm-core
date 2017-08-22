import reversion
from django.db import models

from idm_core.application.mixins import ManageableModel
from idm_core.contact.mixins import Contactable
from idm_core.identity.models import IdentityBase

# ISO/IEC 5218
SEX_CHOICES = (
    ('0', 'not known'),
    ('1', 'male'),
    ('2', 'female'),
    ('9', 'not applicable'),
)


class Person(ManageableModel, IdentityBase):
    type_slug = 'person'

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')
    primary_name = models.OneToOneField('name.Name', related_name='primary_name_of', null=True, blank=True, default=None)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    deceased = models.BooleanField(default=False)

    def _merge(self, others, other_ids):
        super()._merge(others, other_ids)

        fields_to_copy = {'date_of_birth', 'date_of_death', 'deceased'}
        for other in others:
            for field_name in fields_to_copy:
                if getattr(other, field_name) and not getattr(self, field_name):
                    setattr(self, field_name, getattr(other, field_name))
            if other.sex != '0' and self.sex == '0':
                self.sex = other.sex

    def save(self, *args, **kwargs):
        from ..name.models import Name
        try:
            self.label = self.primary_name.plain
            self.qualified_label = self.primary_name.plain_full
            self.sort_label = self.primary_name.sort
        except (Name.DoesNotExist, AttributeError):
            self.label, self.qualified_label, self.sort_label = '', '', ''
        return super().save(*args, **kwargs)

reversion.register(Person)
