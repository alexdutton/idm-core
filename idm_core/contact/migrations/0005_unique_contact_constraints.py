from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20170615_1420'),
    ]

    operations = [
        migrations.RunSQL(
            ("CREATE UNIQUE INDEX contact_onlineaccount_unique ON contact_onlineaccount (provider_id, screen_name) "
             "WHERE validated"),
            "DROP INDEX contact_onlineaccount_unique"
        ),
        migrations.RunSQL(
            "CREATE UNIQUE INDEX contact_email_unique ON contact_email (value) WHERE validated",
            "DROP INDEX contact_email_unique"
        ),
    ]
