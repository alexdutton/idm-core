import django_fsm
from django.db import models

IMAGE_STATE_CHOICES = (
    ('proposed', 'proposed'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
    ('previous', 'previous'),
)


class AcceptableModel(models.Model):
    subject_to_acceptance = True
    only_one_accepted = True

    def get_acceptance_queryset(self):
        return type(self).objects.all()

    state = django_fsm.FSMField(choices=IMAGE_STATE_CHOICES, default='proposed')

    @django_fsm.transition(state, source=['proposed', 'rejected'], target='accepted')
    def accept(self):
        if self.only_one_accepted:
            for obj in self.get_acceptance_queryset().filter(state='accepted').select_for_update():
                obj.retire()
                obj.save()

    @django_fsm.transition(state, source=['proposed', 'accepted'], target='rejected')
    def reject(self):
        pass

    @django_fsm.transition(state, source='*', target='previous')
    def retire(self):
        pass

    def get_acceptance_queryset(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        # If this one is proposed, delete any other proposed objects
        if self.state == 'proposed' and self.only_one_accepted:
            self.get_acceptance_queryset().filter(state='proposed').exclude(pk=self.pk).delete()
        # Wave this one through if it's not subject to acceptance.
        if self.state == 'proposed' and not self.subject_to_acceptance:
            self.accept()
        super().save()

    class Meta:
        abstract = True