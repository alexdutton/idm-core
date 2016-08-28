# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('name', '0002_name_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
