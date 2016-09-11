# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('oxidentity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('supports_object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocument',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(max_length=32, choices=[('driving-license', 'Driving license'), ('passport', 'Passport'), ('national-identity-document', 'National identity document'), ('bill', 'Bill'), ('visa', 'Visa'), ('other', 'Other')])),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('label', models.CharField(blank=True, max_length=256)),
                ('identity', models.ForeignKey(related_name='source_documents', to='oxidentity.Identity')),
                ('validated_by', models.ForeignKey(related_name='validated_source_documents', to='oxidentity.Identity')),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocumentPage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('page_number', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('content_type', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('source_document', models.ForeignKey(to='attestation.SourceDocument')),
            ],
        ),
        migrations.AddField(
            model_name='attestation',
            name='source_document',
            field=models.ForeignKey(to='attestation.SourceDocument'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='supports_content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
    ]
