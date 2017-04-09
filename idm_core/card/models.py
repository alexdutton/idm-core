from django.db import models


class CardStatus(models.Model):
    id = models.CharField(max_length=2)
    label = models.TextField()
