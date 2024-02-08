# Generated by Django 5.0.1 on 2024-02-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_course_day_of_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='days_of_week',
            field=models.ManyToManyField(to='clients.dayofweek'),
        ),
    ]