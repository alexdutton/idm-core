# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idm_identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.TextField()),
                ('alpha_2', models.CharField(max_length=2, unique=True, null=True, db_index=True)),
                ('alpha_3', models.CharField(max_length=3, unique=True, null=True, db_index=True)),
                ('numeric', models.CharField(max_length=3, unique=True, null=True, db_index=True)),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('country', models.ForeignKey(to='nationality.Country')),
                ('identity', models.ForeignKey(to='idm_identity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='country',
            name='identities',
            field=models.ManyToManyField(related_name='nationalities', through='nationality.Nationality', to='idm_identity.Identity'),
        ),
    ]
