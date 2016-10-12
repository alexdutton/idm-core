# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idm_identity', '0002_identity_primary_name'),
        ('attestation', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcedocument',
            name='identity',
            field=models.ForeignKey(to='idm_identity.Identity', related_name='source_documents'),
        ),
        migrations.AddField(
            model_name='sourcedocument',
            name='validated_by',
            field=models.ForeignKey(to='idm_identity.Identity', related_name='validated_source_documents'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='source_document',
            field=models.ForeignKey(to='attestation.SourceDocument'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='supports_content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
    ]
