from django.db import models


class OrganizationTag(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)


class OrganizationRelationshipType(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)


class Organization(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=255)
    realm = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(OrganizationTag, blank=True)

    relationships = models.ManyToManyField(to='self', through='OrganizationRelationship', symmetrical=False)

    def __str__(self):
        return self.label


class OrganizationRelationship(models.Model):
    type = models.ForeignKey(OrganizationRelationshipType)
    subject = models.ForeignKey(Organization, related_name='relationship')
    object = models.ForeignKey(Organization, related_name='incoming_relationship')

