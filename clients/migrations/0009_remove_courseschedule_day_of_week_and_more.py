# Generated by Django 5.0.2 on 2024-02-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_client_assigned_laptop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseschedule',
            name='day_of_week',
        ),
        migrations.RemoveField(
            model_name='courseschedule',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='courseschedule',
            name='days',
            field=models.ManyToManyField(blank=True, related_name='course_schedules', to='clients.dayofweek'),
        ),
        migrations.AlterField(
            model_name='dayofweek',
            name='name',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=20),
        ),
    ]
