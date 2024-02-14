# Generated by Django 5.0.1 on 2024-02-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_resource_client_alter_resource_course'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together={('seat_number', 'course')},
        ),
        migrations.AlterField(
            model_name='resource',
            name='seat_number',
            field=models.CharField(choices=[('seat_1', 'Seat 1'), ('seat_2', 'Seat 2'), ('seat_3', 'Seat 3'), ('seat_4', 'Seat 4'), ('seat_5', 'Seat 5'), ('seat_6', 'Seat 6'), ('seat_7', 'Seat 7'), ('seat_8', 'Seat 8'), ('seat_9', 'Seat 9'), ('seat_10', 'Seat 10'), ('seat_11', 'Seat 11'), ('seat_12', 'Seat 12')], max_length=10, unique=True),
        ),
        migrations.RemoveField(
            model_name='resource',
            name='room',
        ),
    ]