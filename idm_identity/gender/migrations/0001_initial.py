# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('iso_5218', models.CharField(max_length=1)),
                ('pronouns', models.TextField(blank=True, help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]')),
            ],
        ),
    ]
