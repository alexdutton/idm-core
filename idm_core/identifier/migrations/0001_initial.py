# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=64)),
            ],
        ),
    ]