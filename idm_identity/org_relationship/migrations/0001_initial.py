# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm
import idm_identity.org_relationship.models


class Migration(migrations.Migration):

    dependencies = [
        ('idm_identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(max_length=16, choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], protected=True, db_index=True)),
                ('suspended', idm_identity.org_relationship.models.FSMBooleanField(default=False, protected=True, db_index=True)),
                ('job_title', models.CharField(max_length=256, blank=True)),
                ('course_id', models.CharField(max_length=256, blank=True)),
                ('dependent_on', models.ForeignKey(blank=True, to='org_relationship.Affiliation', null=True)),
                ('identity', models.ForeignKey(to='idm_identity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AffiliationType',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('edu_person_affiliation_value', models.CharField(max_length=32, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('realm', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRole',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('organization', models.ForeignKey(to='org_relationship.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(max_length=16, choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], protected=True, db_index=True)),
                ('suspended', idm_identity.org_relationship.models.FSMBooleanField(default=False, protected=True, db_index=True)),
                ('dependent_on', models.ForeignKey(blank=True, to='org_relationship.Role', null=True)),
                ('identity', models.ForeignKey(to='idm_identity.Identity')),
                ('organization', models.ForeignKey(to='org_relationship.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.ForeignKey(to='org_relationship.RoleType'),
        ),
        migrations.AddField(
            model_name='organizationrole',
            name='type',
            field=models.ForeignKey(to='org_relationship.RoleType'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='organization',
            field=models.ForeignKey(to='org_relationship.Organization'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='type',
            field=models.ForeignKey(to='org_relationship.AffiliationType'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationrole',
            unique_together=set([('type', 'organization')]),
        ),
    ]
