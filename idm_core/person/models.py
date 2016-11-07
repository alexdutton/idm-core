import uuid

import reversion
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django_fsm import FSMField, transition
import templated_email

# ISO/IEC 5218
SEX_CHOICES = (
    ('0', 'not known'),
    ('1', 'male'),
    ('2', 'female'),
    ('9', 'not applicable'),
)

STATE_CHOICES = (
    ('new', 'new'),
    ('pending_claim', 'pending claim'),
    ('active', 'active'),
    ('dormant', 'dormant'),
    ('merged', 'merged'),
)

def get_uuid():
    return uuid.uuid4().hex


class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    person = models.ForeignKey('Person', null=True, blank=True)


class Person(DirtyFieldsMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid, editable=False)

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')

    primary_name = models.OneToOneField('name.Name', related_name='primary_name_of', null=True, blank=True, default=None)

    primary_email = models.EmailField(blank=True)
    primary_username = models.CharField(blank=True, max_length=32)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    deceased = models.BooleanField(default=False)

    state = FSMField(choices=STATE_CHOICES, default='new')
    # matriculation_date
    # photo

    claim_code = models.UUIDField(null=True, blank=True)

    merged_into = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'identities'

    def natural_key(self):
        return self.uuid

    def __str__(self):
        try:
            return self.primary_name.plain
        except Exception:
            return self.primary_email or str(self.id)

    @transition(field=state, source='new', target='pending_claim',
                conditions=[lambda self: self.emails.exists()])
    def ready_for_claim(self, email=None):
        if not email:
            email = self.emails.order_by('order').first().value
        self.claim_code = get_uuid()
        templated_email.send_templated_mail(template_name='claim-person',
                                            from_email=settings.DEFAULT_FROM_EMAIL,
                                            to_email=email,
                                            context={'person': self,
                                                     'claim_url': settings.CLAIM_URL.format(self.claim_code)})

    @transition(field=state, source='pending_claim', target='active')
    def claimed(self):
        pass

    @transition(field=state, source='active', target='dormant')
    def set_dormant(self):
        pass

    @transition(field=state, source='dormant', target='active')
    def unset_dormant(self):
        pass

    @transition(field=state, source='*', target='merged')
    def merge_into(self, other):
        self.merged_into = other

reversion.register(Person)
