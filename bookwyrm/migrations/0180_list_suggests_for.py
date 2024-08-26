# Generated by Django 3.2.20 on 2023-08-01 13:12

import bookwyrm.models.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bookwyrm", "0179_populate_sort_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="list",
            name="suggests_for",
            field=bookwyrm.models.fields.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="suggestion_list",
                to="bookwyrm.edition",
            ),
        ),
    ]