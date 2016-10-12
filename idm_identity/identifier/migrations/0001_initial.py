# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=64)),
            ],
        ),
    ]
