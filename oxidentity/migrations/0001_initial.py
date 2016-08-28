# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dirtyfields.dirtyfields
import oxidentity.models


class Migration(migrations.Migration):

    dependencies = [
        ('gender', '0001_initial'),
        ('name', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('uuid', models.UUIDField(serialize=False, editable=False, primary_key=True, default=oxidentity.models.get_uuid)),
                ('pronouns', models.TextField(blank=True, help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]')),
                ('primary_email', models.EmailField(max_length=254, blank=True)),
                ('primary_username', models.CharField(max_length=32, blank=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True)),
                ('deceased', models.BooleanField(default=False)),
                ('gender', models.ForeignKey(related_name='people', blank=True, to='gender.Gender', null=True)),
                ('legal_gender', models.ForeignKey(related_name='people_legally', blank=True, to='gender.Gender', null=True)),
                ('merged_into', models.ForeignKey(blank=True, to='oxidentity.Person', null=True)),
                ('primary_name', models.OneToOneField(related_name='primary_name_of', to='name.Name', blank=True, null=True, default=None)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
