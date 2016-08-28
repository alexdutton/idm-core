# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('name', '0001_initial'),
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='person',
            field=models.ForeignKey(related_name='names', to='oxidentity.Person'),
        ),
    ]
