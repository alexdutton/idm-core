import celery.app.control
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django_fsm import FSMField, transition, RETURN_VALUE, FSMFieldMixin

from idm_core.delayed_save.models import DelayedSave
from idm_core.models import Identity
from idm_core.organization.models import Organization


class FSMBooleanField(FSMFieldMixin, models.BooleanField):
    """
    Same as FSMField, but stores the state value in a BooleanField.
    """
    pass

STATE_CHOICES = (
    ('declined', 'Declined'),
    ('offered', 'Offered'),
    ('requested', 'Requested'),
    ('active', 'Active'),
    ('forthcoming', 'Forthcoming'),
    ('historic', 'Historic'),
    ('suspended', 'Suspended'),
)


def is_owning_identity(instance, user):
    return user.identity == instance.identity


class RelationshipType(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class Relationship(models.Model):
    identity = models.ForeignKey(Identity)
    organization = models.ForeignKey(Organization)
#    type = models.ForeignKey(RelationshipType)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    effective_start_date = models.DateTimeField(null=True, blank=True)
    effective_end_date = models.DateTimeField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    suspended_until = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    dependent_on = models.ForeignKey('self', null=True, blank=True)

    state = FSMField(max_length=16, choices=STATE_CHOICES, db_index=True, protected=True)
    suspended = FSMBooleanField(db_index=True, default=False, protected=True)

    delayed_save = GenericRelation(DelayedSave)

    class Meta:
        abstract = True

    def schedule_resave(self):
        now = timezone.now()
        dates = [self.start_date,
                 self.end_date,
                 self.effective_start_date,
                 self.effective_end_date,
                 self.review_date,
                 self.suspended_until]
        dates = sorted(d for d in dates if d and d > now)

        if dates:
            try:
                delayed_save = self.delayed_save.get()
            except DelayedSave.DoesNotExist:
                delayed_save = DelayedSave(object=self)
            delayed_save.when = dates[0]
            delayed_save.save()
        elif self.delayed_save.exists():
            self.delayed_save.get().delete()

    @property
    def extant(self):
        now = timezone.now()
        return (not (self.effective_start_date or self.start_date) or \
                (self.effective_start_date or self.start_date) < now) and \
               (not (self.effective_end_date or self.end_date) or \
                (self.effective_end_date or self.end_date) > now)

    @transition(field=suspended, source=True, target=False)
    def unsuspend(self):
        self.suspended_until = None
        if self.state == 'suspended':
            self._unsuspend_state()

    @transition(field=suspended, source=False, target=True)
    def suspend(self, until=None):
        self.suspended_until = until
        if self.state == 'active':
            self._suspend_state()

    @transition(field=state, source='suspended', target='active')
    def _unsuspend_state(self):
        pass

    @transition(field=state, source='active', target='suspended')
    def _suspend_state(self):
        pass

    @transition(field=state, source='offered', target=RETURN_VALUE(),
                permission=is_owning_identity)
    def accept(self):
        return self._time_has_passed(now_active=True)

    @transition(field=state, source='offered', target='rejected',
                permission=is_owning_identity)
    def reject(self):
        pass

    @transition(field=state, source='*', target=RETURN_VALUE())
    def _time_has_passed(self, now_active=False):
        start_date = self.effective_start_date or self.start_date
        end_date = self.effective_end_date or self.end_date
        now = timezone.now()

        if self.state == 'suspended' and self.suspended_until and self.suspended_until < now:
            self.unsuspend()

        if now_active or self.state in {'forthcoming', 'active', 'historic', ''}:
            if start_date <= now and (not end_date or now <= end_date):
                return 'active' if not self.suspended else 'suspended'
            elif now < start_date:
                return 'forthcoming'
            elif end_date < now:
                return 'historic'
        else:
            return self.state

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now()
        self._time_has_passed()
        super().save(*args, **kwargs)
        self.schedule_resave()


class RoleType(RelationshipType):
    """
    e.g. bursar, ITSS, information custodian
    """
    # Role, in w3c org ontology terms
    pass


class OrganizationRole(models.Model):
    """
    A relationship between an organization and a role
    """
    # Post, in w3c org ontology terms
    type = models.ForeignKey(RoleType)
    organization = models.ForeignKey(Organization)
    label = models.CharField(max_length=255)

    class Meta:
        unique_together = (('type', 'organization'),)


class Role(Relationship):
    # Membership, in w3c org ontology terms
    type = models.ForeignKey(RoleType)

    @cached_property
    def organization_role(self):
        try:
            return OrganizationRole.objects.get(type=self.type, organization=self.organization)
        except OrganizationRole.DoesNotExist:
            return OrganizationRole.objects.create(type=self.type, organization=self.organization)

    def save(self, *args, **kwargs):
        self.organization_role
        return super().save(*args, **kwargs)


class AffiliationType(RelationshipType):
    edu_person_affiliation_value = models.CharField(max_length=32, blank=True)


class Affiliation(Relationship):
    type = models.ForeignKey(AffiliationType)

    #metadata = JSONField(default={})
    # location
