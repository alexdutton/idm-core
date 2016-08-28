# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0002_person_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('effective_start_date', models.DateTimeField(null=True, blank=True)),
                ('effective_end_date', models.DateTimeField(null=True, blank=True)),
                ('review_date', models.DateTimeField(null=True, blank=True)),
                ('suspended', models.BooleanField(default=False)),
                ('suspended_until', models.DateTimeField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('dependent_on', models.ForeignKey(null=True, to='org_relationship.Affiliation', blank=True)),
                ('person', models.ForeignKey(to='oxidentity.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AffiliationType',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=32, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('effective_start_date', models.DateTimeField(null=True, blank=True)),
                ('effective_end_date', models.DateTimeField(null=True, blank=True)),
                ('review_date', models.DateTimeField(null=True, blank=True)),
                ('suspended', models.BooleanField(default=False)),
                ('suspended_until', models.DateTimeField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('dependent_on', models.ForeignKey(null=True, to='org_relationship.Role', blank=True)),
                ('person', models.ForeignKey(to='oxidentity.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=32, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=32, serialize=False)),
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
