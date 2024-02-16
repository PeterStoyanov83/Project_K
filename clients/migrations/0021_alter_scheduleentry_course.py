# Generated by Django 5.0.2 on 2024-02-16 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_alter_scheduleentry_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleentry',
            name='course',
            field=models.ForeignKey(default='-----', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_entries', to='clients.course'),
        ),
    ]
