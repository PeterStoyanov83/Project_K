import os
import django
import random
from faker import Faker
from django.core.management.base import BaseCommand
from clients.models import Client, Course, ClientFile


# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_K.settings')
django.setup()

random_pdfs_folder = os.path.join(os.getcwd(), 'random_pdfs')


class Command(BaseCommand):
    help = 'Populate data for your models'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        fake = Faker()

        # Create clients
        for _ in range(10):
            Client.objects.create(
                name=fake.name(),
                location=random.choice([choice[0] for choice in Client.LOCATION_CHOICES]),
                date_of_entry=fake.date_this_decade(),
                signed_agreement=fake.boolean(chance_of_getting_true=50)
            )

        # Create courses
        for _ in range(5):
            Course.objects.create(
                name=fake.word(),
                description=fake.text(),
                start_date=fake.date_this_decade(),
                end_date=fake.date_between(start_date="+30d", end_date="+60d"),
                day_of_week=random.choice([choice[0] for choice in Course.DAY_OF_WEEK_CHOICES]),
                time_slot=random.choice([choice[0] for choice in Course.TIME_SLOT_CHOICES])
            )

        # Create client files (assuming you have files to upload)
        for client in Client.objects.all():
            # List all files in the folder
            files_in_folder = [f for f in os.listdir(random_pdfs_folder) if
                               os.path.isfile(os.path.join(random_pdfs_folder, f))]

            # Choose a random file from the list
            random_file = random.choice(files_in_folder)

            # Create the ClientFile object
            ClientFile.objects.create(
                client=client,
                file=os.path.join('random_pdfs', random_file)
            )
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))
