# Generated by Django 3.2.16 on 2022-12-27 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookwyrm", "0172_alter_user_preferred_language"),
    ]

    operations = [
        migrations.AddField(
            model_name="edition",
            name="audiobook_play_time",
            field=models.DurationField(blank=True, null=True),
        ),
    ]
