# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm
import dirtyfields.dirtyfields
import oxidentity.models


class Migration(migrations.Migration):

    dependencies = [
        ('gender', '0001_initial'),
        ('name', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False, default=oxidentity.models.get_uuid)),
                ('pronouns', models.TextField(help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]', blank=True)),
                ('primary_email', models.EmailField(max_length=254, blank=True)),
                ('primary_username', models.CharField(max_length=32, blank=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True)),
                ('deceased', models.BooleanField(default=False)),
                ('state', django_fsm.FSMField(max_length=50, default='new')),
                ('gender', models.ForeignKey(to='gender.Gender', null=True, blank=True, related_name='people')),
                ('legal_gender', models.ForeignKey(to='gender.Gender', null=True, blank=True, related_name='people_legally')),
                ('merged_into', models.ForeignKey(to='oxidentity.Identity', null=True, blank=True)),
                ('primary_name', models.OneToOneField(to='name.Name', blank=True, null=True, default=None, related_name='primary_name_of')),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False, default=oxidentity.models.get_uuid)),
                ('identity', models.ForeignKey(to='oxidentity.Identity', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
