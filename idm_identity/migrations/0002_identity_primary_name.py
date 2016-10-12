# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('name', '0001_initial'),
        ('idm_identity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identity',
            name='primary_name',
            field=models.OneToOneField(blank=True, to='name.Name', default=None, related_name='primary_name_of', null=True),
        ),
    ]
