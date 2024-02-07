from django.db import models


# Your existing ClientFile and Client models would remain unchanged.

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


class Course(models.Model):
    # Removed the DAY_OF_WEEK_CHOICES replaced with DayOfWeek model.
    # Removed the TIME_SLOT_CHOICES replaced with TimeSlot model.

    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True,
        default=""
    )
    start_date = models.DateField()
    end_date = models.DateField()
    clients = models.ManyToManyField(
        'Client',
        related_name='courses'
    )

    # These are the new fields that relate to the DayOfWeek and TimeSlot models
    days_of_week = models.ManyToManyField(
        DayOfWeek
    )
    time_slots = models.ManyToManyField(
        TimeSlot
    )

    def __str__(self):
        days = ', '.join(day.name for day in self.days_of_week.all())
        times = ', '.join(str(slot) for slot in self.time_slots.all())
        return f"{self.name} ({days} at {times})"


class ClientFile(models.Model):
    file = models.FileField(
        upload_to='client_files/'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.file.name} uploaded on {self.uploaded_at}"


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
    files = models.ManyToManyField(
        ClientFile,
        related_name='clients',

    )

    def __str__(self):
        return self.name
