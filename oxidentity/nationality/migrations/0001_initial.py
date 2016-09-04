# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0002_person_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('label', models.TextField()),
                ('alpha_2', models.CharField(null=True, max_length=2, db_index=True, unique=True)),
                ('alpha_3', models.CharField(null=True, max_length=3, db_index=True, unique=True)),
                ('numeric', models.CharField(null=True, max_length=3, db_index=True, unique=True)),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('country', models.ForeignKey(to='nationality.Country')),
                ('person', models.ForeignKey(to='oxidentity.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='country',
            name='people',
            field=models.ManyToManyField(to='oxidentity.Person', related_name='nationalities', through='nationality.Nationality'),
        ),
    ]
