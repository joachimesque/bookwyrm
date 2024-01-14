# Generated by Django 3.2.23 on 2024-01-14 00:55

import bookwyrm.storage_backends
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookwyrm', '0191_merge_20240102_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookwyrmexportjob',
            name='export_json',
            field=models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AddField(
            model_name='bookwyrmexportjob',
            name='json_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bookwyrmexportjob',
            name='export_data',
            field=models.FileField(null=True, storage=bookwyrm.storage_backends.ExportsFileStorage, upload_to=''),
        ),
        migrations.CreateModel(
            name='AddFileToTar',
            fields=[
                ('childjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookwyrm.childjob')),
                ('parent_export_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_edition_export_jobs', to='bookwyrm.bookwyrmexportjob')),
            ],
            options={
                'abstract': False,
            },
            bases=('bookwyrm.childjob',),
        ),
        migrations.CreateModel(
            name='AddBookToUserExportJob',
            fields=[
                ('childjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bookwyrm.childjob')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookwyrm.edition')),
            ],
            options={
                'abstract': False,
            },
            bases=('bookwyrm.childjob',),
        ),
    ]
