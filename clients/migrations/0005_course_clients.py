# Generated by Django 5.0.1 on 2024-01-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_clientfile_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='clients',
            field=models.ManyToManyField(related_name='courses', to='clients.client'),
        ),
    ]
