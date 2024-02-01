import os
import django
import random
from faker import Faker
from django.utils import timezone
from django.core.management.base import BaseCommand
from clients.models import Client, Course
from admins.models import Admin

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_K.settings')
django.setup()


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Delete existing data
        Client.objects.all().delete()
        Course.objects.all().delete()
        Admin.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))

        # Populate Clients
        for _ in range(50):
            Client.objects.create(
                name=fake.company(),
                location=random.choice(['Office Center', 'Kitchen', 'Studio', 'Meal Service', 'Various'])
            )

        for _ in range(20):
            course_name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
            client = Client.objects.order_by('?').first()  # Random client from the database
            start_date = fake.date_this_year(before_today=False, after_today=True)
            end_date = start_date + timezone.timedelta(days=random.randint(1, 60))
            Course.objects.create(
                name=course_name,
                client=client,
                start_date=start_date,
                end_date=end_date,
                # Assuming 'schedule' and 'time_slot' are CharFields or similar in the Course model
                schedule=fake.sentence(nb_words=4),
                time_slot=random.choice(['08:30-10:00', '10:30-12:00', '13:30-15:00'])
            )

        self.stdout.write(self.style.SUCCESS('Database populated with sample data for courses and clients.'))
