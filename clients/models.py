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

    def __str__(self):
        return self.name


class Course(models.Model):
    PLATFORM_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In-person'),
        ('other', 'Other'),
    ]

    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True,
        default=""
    )
    platform = models.CharField(
        max_length=10,
        choices=PLATFORM_CHOICES,
        default='-----'
    )
    other_platform_comment = models.TextField(
        blank=True,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    clients = models.ManyToManyField(
        'Client',
        related_name='enrolled_courses',  # This related_name is used in the Client model to access courses
        blank=True
    )

    def __str__(self):
        # Fetch related CourseSchedule objects and format their information
        schedules = self.schedules.all()
        schedule_str = ", ".join(f"{schedule.day_of_week} at {schedule.time_slot}" for schedule in schedules)
        return f"{self.name} - Schedule: {schedule_str}"


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courseschedule_set')

    day_of_week = models.CharField(
        max_length=9,
        choices=DAYS_OF_WEEK_CHOICES
    )
    time_slot = models.CharField(
        max_length=11,
        choices=TIME_SLOT_CHOICES
    )


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
    file = models.FileField(
        upload_to='client_files/'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return os.path.basename(self.file.name)


class Resource(models.Model):
    ROOM_CHOICES = [
        ('room_1', 'Room 1'),
        ('room_2', 'Room 2'),
    ]

    room = models.CharField(max_length=6, choices=ROOM_CHOICES)
    seat_number = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('room', 'seat_number'),  # No two resources can have the same room, seat_number, and course
            ('client', 'course'),  # A client cannot be assigned more than one seat in the same course
        )

    def __str__(self):
        # The course does not need to be mentioned in the string representation if not needed.
        return f"{self.get_room_display()} Seat {self.seat_number} - {self.client.name}"


class Laptop(models.Model):
    LAPTOP_CHOICES = [
        ('laptop1', 'Laptop 1'),
        ('laptop2', 'Laptop 2'),
        ('laptop3', 'Laptop 3'),
        ('laptop4', 'Laptop 4'),
    ]
    name = models.CharField(
        max_length=10,
        choices=LAPTOP_CHOICES,
        unique=True)
    assigned_to = models.ForeignKey(
        Client,
        related_name='assigned_laptops',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    period_start = models.DateField()
    period_end = models.DateField()
    comments = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.get_name_display()
