# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('value', models.CharField(max_length=64)),
                ('identity', models.ForeignKey(to='oxidentity.Identity')),
            ],
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='identifier',
            name='type',
            field=models.ForeignKey(to='identifier.IdentifierType'),
        ),
        migrations.AlterUniqueTogether(
            name='identifier',
            unique_together=set([('type', 'value'), ('type', 'identity')]),
        ),
        migrations.AlterIndexTogether(
            name='identifier',
            index_together=set([('type', 'value'), ('type', 'identity')]),
        ),
    ]
