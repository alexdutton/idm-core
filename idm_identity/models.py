import uuid

import reversion
from dirtyfields import DirtyFieldsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django_fsm import FSMField, transition

from .gender.models import Gender


def get_uuid():
    return uuid.uuid4().hex


class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    identity = models.ForeignKey('Identity', null=True, blank=True)


class Identity(DirtyFieldsMixin, models.Model):
    uuid = models.UUIDField(primary_key=True, default=get_uuid, editable=False)

    gender = models.ForeignKey(Gender, null=True, blank=True, related_name='people')
    legal_gender = models.ForeignKey(Gender, null=True, blank=True, related_name='people_legally',
                                     limit_choices_to=['male', 'female'])
    pronouns = models.TextField(blank=True,
                                help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]')
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
                conditions=[lambda self: self.primary_email is not None])
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