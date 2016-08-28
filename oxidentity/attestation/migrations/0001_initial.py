# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oxidentity', '0002_person_state'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supports_object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('driving-license', 'Driving license'), ('passport', 'Passport'), ('national-identity-document', 'National identity document'), ('bill', 'Bill'), ('visa', 'Visa'), ('other', 'Other')], max_length=32)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('label', models.CharField(blank=True, max_length=256)),
                ('person', models.ForeignKey(to='oxidentity.Person', related_name='source_documents')),
                ('validated_by', models.ForeignKey(to='oxidentity.Person', related_name='validated_source_documents')),
            ],
        ),
        migrations.CreateModel(
            name='SourceDocumentPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.PositiveSmallIntegerField(null=True, blank=True)),
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
