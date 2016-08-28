import celery.app.control
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from oxidentity.delayed_save.models import DelayedSave
from oxidentity.models import Person

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

    suspended = models.BooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    dependent_on = models.ForeignKey('self', null=True, blank=True)

    active = models.BooleanField(default=False)

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


    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.suspended and self.suspended_until and self.suspended_until < now:
            self.suspended = False
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