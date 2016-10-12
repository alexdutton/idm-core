from django.db import models


class Gender(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    label = models.CharField(max_length=255)
    iso_5218 = models.CharField(max_length=1)
    pronouns = models.TextField(blank=True,
                                help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]')

    def __str__(self):
        return self.label
