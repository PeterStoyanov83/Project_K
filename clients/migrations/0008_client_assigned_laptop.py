# Generated by Django 5.0.2 on 2024-02-15 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_resource_seat_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='assigned_laptop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_to_client', to='clients.laptop'),
        ),
    ]
