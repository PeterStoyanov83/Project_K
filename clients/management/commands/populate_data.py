import os
import django
import random
from django.core.management.base import BaseCommand
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_K.settings')
django.setup()

from clients.models import Client, ClientFile, Course, DAYS_OF_WEEK_CHOICES, \
    TIME_SLOT_CHOICES, CourseSchedule, Resource  # Import your models here

fake = Faker()


def populate_clients(n=10):
    for _ in range(n):
        name = fake.name()
        location = random.choice(Client.LOCATION_CHOICES)[0]
        date_of_entry = fake.date_between(start_date='-3y', end_date='today')
        date_of_exit = fake.date_between(start_date=date_of_entry, end_date='today') if random.choice(
            [True, False]) else None
        signed_agreement = fake.boolean()

        Client.objects.create(
            name=name,
            location=location,
            date_of_entry=date_of_entry,
            date_of_exit=date_of_exit,
            signed_agreement=signed_agreement,
        )


def populate_course_schedules(n=20):
    courses = Course.objects.all()
    for course in courses:
        # Assuming each course can have multiple schedules
        for _ in range(random.randint(1, 3)):  # Random number of schedules for each course
            day_of_week = random.choice(DAYS_OF_WEEK_CHOICES)[0]
            time_slot = random.choice(TIME_SLOT_CHOICES)[0]
            CourseSchedule.objects.create(
                course=course,
                day_of_week=day_of_week,
                time_slot=time_slot,
            )


def populate_client_files(n=20):
    clients = Client.objects.all()
    for _ in range(n):
        client = random.choice(clients)
        # Assuming you have a way to handle file field. For demonstration, just using a fake file name
        file_name = fake.file_name()
        uploaded_at = fake.date_time_between(start_date='-1y', end_date='now')

        ClientFile.objects.create(
            client=client,  # Ensure this line is uncommented and correctly assigns a client
            file=f"client_files/{file_name}",  # Note: In a real app, you'd need to handle file uploading differently
            uploaded_at=uploaded_at,
        )


def populate_resources():
    courses = Course.objects.all()
    clients = Client.objects.all()
    room_choices = ['room_1', 'room_2']

    for course in courses:
        for client in random.sample(list(clients), k=random.randint(1, min(5, len(clients)))):
            room = random.choice(room_choices)
            seat_number = str(random.randint(1, 8)) if room == 'room_1' else str(random.randint(1, 4))
            Resource.objects.create(
                room=room,
                seat_number=seat_number,
                course=course,
                client=client,
            )


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating Clients...'))
        populate_clients(50)
        self.stdout.write(self.style.SUCCESS('Populating Course Schedules...'))
        populate_course_schedules(15)  # Adjusted to call the correct function
        self.stdout.write(self.style.SUCCESS('Populating ClientFiles...'))
        populate_client_files(100)
        self.stdout.write(self.style.SUCCESS('Populating Resources...'))
        populate_resources()  # Ensure this function is called to populate Resources
        self.stdout.write(self.style.SUCCESS('Data Population Complete!'))
