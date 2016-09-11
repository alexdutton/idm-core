# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm
import oxidentity.org_relationship.models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], max_length=16, protected=True, db_index=True)),
                ('suspended', oxidentity.org_relationship.models.FSMBooleanField(protected=True, db_index=True, default=False)),
                ('job_title', models.CharField(max_length=256, blank=True)),
                ('course_id', models.CharField(max_length=256, blank=True)),
                ('dependent_on', models.ForeignKey(to='org_relationship.Affiliation', null=True, blank=True)),
                ('identity', models.ForeignKey(to='oxidentity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AffiliationType',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], max_length=16, protected=True, db_index=True)),
                ('suspended', oxidentity.org_relationship.models.FSMBooleanField(protected=True, db_index=True, default=False)),
                ('dependent_on', models.ForeignKey(to='org_relationship.Role', null=True, blank=True)),
                ('identity', models.ForeignKey(to='oxidentity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.ForeignKey(to='org_relationship.RoleType'),
        ),
        migrations.AddField(
            model_name='role',
            name='unit',
            field=models.ForeignKey(to='org_relationship.Unit'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='type',
            field=models.ForeignKey(to='org_relationship.AffiliationType'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='unit',
            field=models.ForeignKey(to='org_relationship.Unit'),
        ),
    ]
