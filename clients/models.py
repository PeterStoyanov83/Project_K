# clients/models.py
from django.db import models
import os

DAYS_OF_WEEK_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

TIME_SLOT_CHOICES = [
    ('08:30-10:00', '08:30-10:00'),
    ('10:30-12:00', '10:30-12:00'),
    ('13:30-15:00', '13:30-15:00'),
]


class Client(models.Model):
    LOCATION_CHOICES = [
        ('office_center', 'Office Center'),
        ('kitchen', 'Kitchen'),
        ('studio', 'Studio'),
        ('meal_service', 'Meal Service'),
        ('various', 'Various'),
    ]

    name = models.CharField(
        max_length=50
    )
    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES
    )
    date_of_entry = models.DateField()
    date_of_exit = models.DateField(
        null=True,
        blank=True
    )
    signed_agreement = models.BooleanField(
        default=False
    )

    # files = models.ManyToManyField(ClientFile, related_name='clients')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    clients = models.ManyToManyField('Client', related_name='courses')
    costs = models.FloatField(default=0.00)

    def __str__(self):
        # Fetch related CourseSchedule objects and format their information
        schedules = self.schedules.all()
        schedule_str = ", ".join(f"{schedule.day_of_week} at {schedule.time_slot}" for schedule in schedules)
        return f"{self.name} - Schedule: {schedule_str}"

class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, related_name='schedules', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK_CHOICES)
    time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES)


class DayOfWeek(models.Model):
    name = models.CharField(
        max_length=15
    )

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class ClientFile(models.Model):
    client = models.ForeignKey(
        Client,
        related_name='files',
        on_delete=models.CASCADE,
        null=True
    )
    file = models.FileField(upload_to='client_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.file.name)
