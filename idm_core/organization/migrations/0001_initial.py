# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-11 21:15
from __future__ import unicode_literals

import uuid

import dirtyfields.dirtyfields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import idm_core.identity.models
import idm_core.relationship.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unmanaged_fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, default=[], size=None)),
                ('manage_url', models.URLField(blank=True)),
                ('upstream_id', models.CharField(blank=True, max_length=32, null=True)),
                ('start_date', models.DateTimeField(default=idm_core.relationship.models.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], db_index=True, max_length=16, protected=True)),
                ('suspended', idm_core.relationship.models.FSMBooleanField(db_index=True, default=False, protected=True)),
                ('dependent_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Affiliation')),
                ('identity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('managed_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
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
                ('edu_person_affiliation_value', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('primary_email', models.EmailField(blank=True, max_length=254)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=1024)),
                ('qualified_label', models.CharField(blank=True, max_length=1024)),
                ('sort_label', models.CharField(blank=True, max_length=1024)),
                ('primary_username', models.CharField(blank=True, max_length=32)),
                ('state', django_fsm.FSMField(choices=[('established', 'established'), ('active', 'active'),
                                                       ('archived', 'archived'), ('suspended', 'suspended'),
                                                       ('merged', 'merged')], default='established', max_length=50)),
                ('merged_into', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='merged_from', to='organization.Organization')),
            ],
            options={
                'permissions': (('can_view_affiliates', 'can view affiliated people'),
                                ('can_manage_affiliations', 'can manage affiliations'),
                                ('can_offer_affiliations', 'can manage affiliations'),
                                ('can_manage_roles', 'can manage roles')),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='incoming_relationship', to='organization.Organization')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='relationship', to='organization.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRelationshipType',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRole',
            fields=[
                ('primary_email', models.EmailField(blank=True, max_length=254)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=1024)),
                ('qualified_label', models.CharField(blank=True, max_length=1024)),
                ('sort_label', models.CharField(blank=True, max_length=1024)),
                ('primary_username', models.CharField(blank=True, max_length=32)),
                ('state', django_fsm.FSMField(choices=[('established', 'established'), ('active', 'active'),
                                                       ('archived', 'archived'), ('suspended', 'suspended'),
                                                       ('merged', 'merged')], default='established', max_length=50)),
                ('role_label', models.CharField(max_length=255)),
                ('merged_into', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='merged_from', to='organization.OrganizationRole')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                   to='organization.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationTag',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unmanaged_fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, default=[], size=None)),
                ('manage_url', models.URLField(blank=True)),
                ('upstream_id', models.CharField(blank=True, max_length=32, null=True)),
                ('start_date', models.DateTimeField(default=idm_core.relationship.models.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('effective_start_date', models.DateTimeField(blank=True, null=True)),
                ('effective_end_date', models.DateTimeField(blank=True, null=True)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('suspended_until', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True)),
                ('state', django_fsm.FSMField(choices=[('declined', 'Declined'), ('offered', 'Offered'), ('requested', 'Requested'), ('active', 'Active'), ('forthcoming', 'Forthcoming'), ('historic', 'Historic'), ('suspended', 'Suspended')], db_index=True, max_length=16, protected=True)),
                ('suspended', idm_core.relationship.models.FSMBooleanField(db_index=True, default=False, protected=True)),
                ('dependent_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Role')),
                ('identity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('managed_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization')),
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
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.RoleType'),
        ),
        migrations.AddField(
            model_name='organizationrole',
            name='role_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.RoleType'),
        ),
        migrations.AddField(
            model_name='organizationrelationship',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.OrganizationRelationshipType'),
        ),
        migrations.AddField(
            model_name='organization',
            name='relationships',
            field=models.ManyToManyField(through='organization.OrganizationRelationship', to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='tags',
            field=models.ManyToManyField(blank=True, to='organization.OrganizationTag'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.AffiliationType'),
        ),
    ]
