# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org_relationship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='course_id',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='job_title',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AddField(
            model_name='role',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
