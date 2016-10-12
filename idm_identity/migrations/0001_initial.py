# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm
import dirtyfields.dirtyfields
import idm_identity.models


class Migration(migrations.Migration):

    dependencies = [
        ('gender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=idm_identity.models.get_uuid, editable=False)),
                ('pronouns', models.TextField(blank=True, help_text='subject[ object[ possessive-determiner[ possessive-pronoun[ reflexive]]]]')),
                ('primary_email', models.EmailField(max_length=254, blank=True)),
                ('primary_username', models.CharField(max_length=32, blank=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True)),
                ('deceased', models.BooleanField(default=False)),
                ('state', django_fsm.FSMField(max_length=50, default='new')),
                ('gender', models.ForeignKey(blank=True, to='gender.Gender', related_name='people', null=True)),
                ('legal_gender', models.ForeignKey(blank=True, to='gender.Gender', related_name='people_legally', null=True)),
                ('merged_into', models.ForeignKey(blank=True, to='idm_identity.Identity', null=True)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=idm_identity.models.get_uuid, editable=False)),
                ('identity', models.ForeignKey(blank=True, to='idm_identity.Identity', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
