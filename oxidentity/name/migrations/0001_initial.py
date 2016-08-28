# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('plain', models.TextField(blank=True)),
                ('plain_full', models.TextField(blank=True)),
                ('marked_up', models.TextField(blank=True)),
                ('familiar', models.TextField(blank=True)),
                ('sort', models.TextField(blank=True)),
                ('first', models.TextField(blank=True)),
                ('last', models.TextField(blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NameComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('type', models.CharField(max_length=20, choices=[('title', 'Title'), ('given', 'Given name'), ('middle', 'Middle name'), ('family', 'Family name'), ('suffix', 'Suffix'), ('name', 'Name')])),
                ('value', models.TextField()),
                ('name', models.ForeignKey(related_name='components', to='name.Name')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='NameContext',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='name',
            name='contexts',
            field=models.ManyToManyField(to='name.NameContext'),
        ),
    ]
