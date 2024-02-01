from django.db import models
import datetime

class Client(models.Model):
    LOCATION_CHOICES = [
        ('office_center', 'Office Center'),
        ('kitchen', 'Kitchen'),
        ('studio', 'Studio'),
        ('meal_service', 'Meal Service'),
        ('various', 'Various'),
    ]

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    date_of_entry = models.DateField()
    date_of_exit = models.DateField(null=True, blank=True)
    # Omitting direct relationship to courses for brevity

    def __str__(self):
        return self.name

class Course(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    TIME_SLOT_CHOICES = [
        ('08:30-10:00', '08:30-10:00'),
        ('10:30-12:00', '10:30-12:00'),
        ('13:30-15:00', '13:30-15:00'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.CharField(max_length=9, choices=DAY_OF_WEEK_CHOICES, default='Monday')
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='08:30-10:00')

    def __str__(self):
        return f"{self.name} ({self.day_of_week} at {self.time_slot})"

# Assuming ClientFile remains unchanged for brevity
