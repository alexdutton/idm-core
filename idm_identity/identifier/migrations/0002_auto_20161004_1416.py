# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identifier', '0001_initial'),
        ('idm_identity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identifier',
            name='identity',
            field=models.ForeignKey(to='idm_identity.Identity'),
        ),
        migrations.AddField(
            model_name='identifier',
            name='type',
            field=models.ForeignKey(to='identifier.IdentifierType'),
        ),
        migrations.AlterUniqueTogether(
            name='identifier',
            unique_together=set([('type', 'value'), ('type', 'identity')]),
        ),
        migrations.AlterIndexTogether(
            name='identifier',
            index_together=set([('type', 'value'), ('type', 'identity')]),
        ),
    ]
