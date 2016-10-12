# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('supports_object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(max_length=32, choices=[('driving-license', 'Driving license'), ('passport', 'Passport'), ('national-identity-document', 'National identity document'), ('bill', 'Bill'), ('visa', 'Visa'), ('other', 'Other')])),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('label', models.CharField(max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocumentPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('page_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('content_type', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('source_document', models.ForeignKey(to='attestation.SourceDocument')),
            ],
        ),
    ]
