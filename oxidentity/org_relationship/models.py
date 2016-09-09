import celery.app.control
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition, RETURN_VALUE

from oxidentity.delayed_save.models import DelayedSave
from oxidentity.models import Person


STATE_CHOICES = (
    ('new', 'New'),
    ('declined', 'Declined'),
    ('offered', 'Offered'),
    ('requested', 'Requested'),
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
)

class Unit(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class RelationshipType(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class Relationship(models.Model):
    person = models.ForeignKey(Person)
    unit = models.ForeignKey(Unit)
#    type = models.ForeignKey(RelationshipType)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    effective_start_date = models.DateTimeField(null=True, blank=True)
    effective_end_date = models.DateTimeField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    suspended_until = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    dependent_on = models.ForeignKey('self', null=True, blank=True)

    state = FSMField(max_length=16, choices=STATE_CHOICES, db_index=True, default='new', protected=True)

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

    @transition(field=state, source=['suspended'], target=RETURN_VALUE('active', 'inactive'))
    def unsuspend(self):
        return 'active' if self.extant else 'inactive'

    @transition(field=state, source=['active', 'inactive'], target='suspended')
    def suspend(self):
        pass

    @transition(field=state, source='offered', target=RETURN_VALUE('active', 'inactive'))
    def accept(self):
        return 'active' if self.extant else 'inactive'

    @transition(field=state, source='offered', target='rejected')
    def reject(self):
        pass

cd

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.state == 'suspended' and self.suspended_until and self.suspended_until < now:
            self.state = 'active'
        self.active = (not (self.effective_start_date or self.start_date) or \
                       (self.effective_start_date or self.start_date) < now) and \
                      (not (self.effective_end_date or self.end_date) or \
                       (self.effective_end_date or self.end_date) > now) and \
                      not self.suspended
        super().save(*args, **kwargs)
        self.schedule_resave()


class RoleType(RelationshipType):
    """
    e.g. bursar, ITSS, information custodian
    """
    pass


class Role(Relationship):
    type = models.ForeignKey(RoleType)


class AffiliationType(RelationshipType):
    pass


class Affiliation(Relationship):
    type = models.ForeignKey(AffiliationType)

    job_title = models.CharField(max_length=256, blank=True)
    course_id = models.CharField(max_length=256, blank=True)
    # location