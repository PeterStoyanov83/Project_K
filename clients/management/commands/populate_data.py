import os
import django
import random
from django.core.management.base import BaseCommand
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_K.settings')
django.setup()


from clients.models import Client, ClientFile, Course  # Import your models here

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


def populate_courses(n=5):
    for _ in range(n):
        name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
        description = fake.text(max_nb_chars=200)
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+1y')
        day_of_week = random.choice(Course.DAY_OF_WEEK_CHOICES)[0]
        time_slot = random.choice(Course.TIME_SLOT_CHOICES)[0]

        course = Course.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            day_of_week=day_of_week,
            time_slot=time_slot,
        )

        # Optionally, associate some clients with this course
        clients = list(Client.objects.all())
        for client in random.sample(clients, k=random.randint(1, min(5, len(clients)))):
            course.clients.add(client)


def populate_client_files(n=20):
    clients = Client.objects.all()
    for _ in range(n):
        client = random.choice(clients)
        # Assuming you have a way to handle file field. For demonstration, just using a fake file name
        file_name = fake.file_name()
        uploaded_at = fake.date_time_between(start_date='-1y', end_date='now')

        ClientFile.objects.create(
            #client=client,
            file=f"client_files/{file_name}",  # Note: In a real app, you'd need to handle file uploading differently
            uploaded_at=uploaded_at,
        )


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating Clients...'))
        populate_clients(10)
        self.stdout.write(self.style.SUCCESS('Populating Courses...'))
        populate_courses(5)
        self.stdout.write(self.style.SUCCESS('Populating ClientFiles...'))
        populate_client_files(20)
        self.stdout.write(self.style.SUCCESS('Populating Complete!'))
