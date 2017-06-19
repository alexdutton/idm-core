# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-11 21:15
from __future__ import unicode_literals

import dirtyfields.dirtyfields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import idm_core.name.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attested_by', django.contrib.postgres.fields.ArrayField(base_field=models.SlugField(), blank=True, default=[], size=None)),
                ('plain', models.TextField(blank=True)),
                ('plain_full', models.TextField(blank=True)),
                ('marked_up', models.TextField(blank=True)),
                ('familiar', models.TextField(blank=True)),
                ('sort', models.TextField(blank=True)),
                ('first', models.TextField(blank=True)),
                ('last', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('components', idm_core.name.fields.JSONSchemaField(schema={})),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NameContext',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='name',
            name='context',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name.NameContext'),
        ),
    ]
