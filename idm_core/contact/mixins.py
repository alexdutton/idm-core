from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Contactable(models.Model):
    emails = GenericRelation('contact.Email', 'identity_id', 'identity_content_type')
    telephones = GenericRelation('contact.Telephone', 'identity_id', 'identity_content_type')
    addresses = GenericRelation('contact.Address', 'identity_id', 'identity_content_type')
    online_accounts = GenericRelation('contact.OnlineAccount', 'identity_id', 'identity_content_type')

    primary_email = models.EmailField(blank=True)

    class Meta:
        abstract = True
