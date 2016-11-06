# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validated', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('person', 'order'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactContext',
            fields=[
                ('id', models.SlugField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validated', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('value', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ('person', 'order'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Telephone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validated', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('value', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ('person', 'order'),
                'abstract': False,
            },
        ),
    ]
