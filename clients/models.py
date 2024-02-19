# clients/models.py
from django.contrib.auth.models import User
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

    assigned_laptop = models.ForeignKey(
        'Laptop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_to_client'
    )


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
        return f"{self.name}"

    # def __str__(self):
    #     schedule_entries = CourseSchedule.objects.filter(course=self).values_list('schedule_entries', flat=True)
    #     entries_str_list = []
    #     for entry_id in schedule_entries:
    #         try:
    #             entry = ScheduleEntry.objects.get(id=entry_id)
    #             entries_str_list.append(str(entry))
    #         except ScheduleEntry.DoesNotExist:
    #             continue
    #     schedule_str = ", ".join(entries_str_list)
    #     return f"{self.name} - Schedule: {schedule_str}"


class DayOfWeek(models.Model):
    name = models.CharField(
        choices=DAYS_OF_WEEK_CHOICES,
        max_length=20,
    )

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class ScheduleEntry(models.Model):
    monday = models.BooleanField(default=False)
    monday_time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True, blank=True)

    tuesday = models.BooleanField(default=False)
    tuesday_time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True, blank=True)

    wednesday = models.BooleanField(default=False)
    wednesday_time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True, blank=True)

    thursday = models.BooleanField(default=False)
    thursday_time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True, blank=True)

    friday = models.BooleanField(default=False)
    friday_time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True, blank=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedule_entries')

    def __str__(self):
        days_str = []
        for day, slot in [
            ('Monday', self.monday_time_slot),
            # Repeat for other days
        ]:
            if getattr(self, day.lower()):
                days_str.append(f"{day}: {slot or 'No time slot selected'}")
        return f"{self.course.name} - {'; '.join(days_str)}"

    def get_schedule_display(self):
        days_str = []
        for day, slot in [
            ('Monday', self.monday_time_slot),
            ('Tuesday', self.tuesday_time_slot),
            ('Wednesday', self.wednesday_time_slot),
            ('Thursday', self.thursday_time_slot),
            ('Friday', self.friday_time_slot)
        ]:
            if getattr(self, day.lower()):
                days_str.append(f"{day}: {slot or 'No time slot selected'}")
        return ', '.join(days_str)


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    entries = models.ManyToManyField(ScheduleEntry, through='CourseScheduleEntry', related_name='course_schedules',
                                     blank=True)

    def __str__(self):
        return f"{self.course.name} - Schedule: {', '.join(str(entry) for entry in self.entries.all())}"


class CourseScheduleEntry(models.Model):
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)
    schedule_entry = models.ForeignKey(ScheduleEntry, on_delete=models.CASCADE)


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
    SEAT_CHOICES = [(f'seat_{i}', f'Seat {i}') for i in range(1, 13)]

    seat_number = models.CharField(
        max_length=10,
        choices=SEAT_CHOICES,
        blank=True,
        null=True,
        unique=False
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = (
            ('seat_number', 'course'),  # A seat can't be assigned to multiple courses at once
        )

    def __str__(self):
        client_name = self.client.name if self.client else "No client assigned"
        return f"{self.seat_number} - {client_name}"

    def display_assigned_laptops(self):
        return ', '.join([laptop.name for laptop in self.laptops.all()])

    display_assigned_laptops.short_description = "Assigned Laptops"


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
        unique=True
    )
    assigned_to = models.ForeignKey(
        Client,
        related_name='assigned_client_laptops',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    assigned_to_resource = models.ForeignKey(
        Resource,
        related_name='laptops',  # Specify a related_name for the relationship
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


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
