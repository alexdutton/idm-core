import uuid

import reversion
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django_fsm import FSMField, transition
# ISO/IEC 5218
SEX_CHOICES = (
    ('0', 'not known'),
    ('1', 'male'),
    ('2', 'female'),
    ('9', 'not applicable'),
)

def get_uuid():
    return uuid.uuid4().hex


class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    identity = models.ForeignKey('Identity', null=True, blank=True)


class Identity(DirtyFieldsMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid, editable=False)

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')

    primary_name = models.OneToOneField('name.Name', related_name='primary_name_of', null=True, blank=True, default=None)

    primary_email = models.EmailField(blank=True)
    primary_username = models.CharField(blank=True, max_length=32)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    deceased = models.BooleanField(default=False)

    state = FSMField(default='new')
    # matriculation_date
    # photo

    def natural_key(self):
        return self.uuid

    merged_into = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        try:
            return self.primary_name.plain
        except Exception:
            return super(Identity, self).__str__()

    @transition(field=state, source='new', target='pending_claim',
                conditions=[lambda self: self.emails.exists()])
    def ready_for_claim(self):
        pass

    @transition(field=state, source='pending_claim', target='active')
    def claimed(self):
        pass

    @transition(field=state, source='active', target='dormant')
    def set_dormant(self):
        pass

    @transition(field=state, source='dormant', target='active')
    def unset_dormant(self):
        pass



reversion.register(Identity)
