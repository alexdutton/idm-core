# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idm_identity', '0001_initial'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='identity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='idm_identity.Identity'),
        ),
    ]