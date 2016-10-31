# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('name', '0001_initial'),
        ('idm_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identity',
            name='primary_name',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_name_of', to='name.Name'),
        ),
    ]
