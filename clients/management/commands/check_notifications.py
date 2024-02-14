from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from clients.models import Course, Client
from clients.models import Notification  # Change 'your_app' to the actual app name


class Command(BaseCommand):
    help = 'Check for clients finishing courses and create notifications'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        notification_messages = []

        # Check for clients finishing a course
        for course in Course.objects.all():
            if today > course.end_date - timedelta(days=5):  # If within 5 days of course ending
                for client in course.clients.all():
                    message = f"{client.name} is finishing {course.name} soon."
                    notification_messages.append((client.user, message))  # Assuming Client has a related User

        # Check for clients with enrollment ending
        for client in Client.objects.filter(date_of_exit__isnull=False):
            if today > client.date_of_exit - timedelta(days=5):  # If within 5 days of enrollment ending
                message = f"{client.name}'s enrollment period is ending soon."
                notification_messages.append((client.user, message))

        # Create notifications
        for user, message in notification_messages:
            Notification.objects.create(user=user, message=message)
