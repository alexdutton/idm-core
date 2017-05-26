from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contact', '0002_auto_20170429_0910'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE UNIQUE INDEX contact_email_verified_unique ON contact_email (value) WHERE validated;",
            "DROP INDEX contact_email_verified_unique;",
        )
    ]