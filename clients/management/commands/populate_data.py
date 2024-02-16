import os
import django
import random
from django.core.management.base import BaseCommand
from faker import Faker

from clients.models import Client, ClientFile, Course, DAYS_OF_WEEK_CHOICES, \
    TIME_SLOT_CHOICES, Resource, ScheduleEntry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_K.settings')
django.setup()

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


def populate_schedule_entries(n=20):
    courses = Course.objects.all()
    time_slots = [slot[0] for slot in TIME_SLOT_CHOICES]

    for _ in range(n):
        course = random.choice(courses)
        # Create a ScheduleEntry for each day the course runs
        for day, _ in DAYS_OF_WEEK_CHOICES:
            if random.choice([True, False]):  # Randomly decide if there's a class on this day
                time_slot = random.choice(time_slots)
                ScheduleEntry.objects.create(
                    course=course,
                    **{f"{day.lower()}": True},
                    **{f"{day.lower()}_time_slot": time_slot}
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
    seat_numbers = [seat[0] for seat in Resource.SEAT_CHOICES]

    for course in courses:
        for client in random.sample(list(clients), k=random.randint(1, min(5, len(clients)))):
            seat_number = random.choice(seat_numbers)

            if not Resource.objects.filter(seat_number=seat_number, course=course).exists():
                Resource.objects.create(
                    seat_number=seat_number,
                    course=course,
                    client=client,
                )


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating Clients...'))
        populate_clients(50)
        self.stdout.write(self.style.SUCCESS('Populating Schedule Entries...'))
        populate_schedule_entries(15)
        self.stdout.write(self.style.SUCCESS('Populating ClientFiles...'))
        populate_client_files(100)
        self.stdout.write(self.style.SUCCESS('Populating Resources...'))
        populate_resources()  # Ensure this function is called to populate Resources
        self.stdout.write(self.style.SUCCESS('Data Population Complete!'))
