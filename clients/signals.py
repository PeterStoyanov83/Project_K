from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import ScheduleEntry, Client, DAYS_OF_WEEK_CHOICES
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ScheduleEntry)
def check_schedule_conflicts(sender, instance, **kwargs):
    # Fetch clients enrolled in the course linked to the saved schedule entry
    clients = Client.objects.filter(enrolled_courses=instance.course)
    logger.debug('Signal handler executed for ScheduleEntry id: %s', instance.pk)

    for client in clients:
        # Fetch all schedule entries for all courses the client is enrolled in
        schedule_entries = ScheduleEntry.objects.filter(course__clients=client)

        # Initialize a dict to keep track of time slots for each day
        day_time_slots = {day[0]: [] for day in DAYS_OF_WEEK_CHOICES}

        for entry in schedule_entries:
            for day, _ in DAYS_OF_WEEK_CHOICES:
                if getattr(entry, day.lower()):
                    time_slot = getattr(entry, f"{day.lower()}_time_slot")
                    if time_slot in day_time_slots[day] and entry.course == instance.course:
                        # Conflict detected: the same client has been scheduled for another course at the same time slot
                        print(
                            f"Conflict detected for {client.name} in {day} at {time_slot} for course {entry.course.name}.")
                    else:
                        day_time_slots[day].append(time_slot)