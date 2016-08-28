# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='state',
            field=django_fsm.FSMField(default='new', max_length=50),
        ),
    ]
