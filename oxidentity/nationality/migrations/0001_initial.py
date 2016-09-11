# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('label', models.TextField()),
                ('alpha_2', models.CharField(unique=True, max_length=2, db_index=True, null=True)),
                ('alpha_3', models.CharField(unique=True, max_length=3, db_index=True, null=True)),
                ('numeric', models.CharField(unique=True, max_length=3, db_index=True, null=True)),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('country', models.ForeignKey(to='nationality.Country')),
                ('identity', models.ForeignKey(to='oxidentity.Identity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='country',
            name='identities',
            field=models.ManyToManyField(through='nationality.Nationality', related_name='nationalities', to='oxidentity.Identity'),
        ),
    ]
