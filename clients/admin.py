# clients/admin.py
from django.contrib import admin
from django.core.checks import messages
from django.db.models import Q

from .models import (Client,
                     ClientFile,
                     Course,
                     CourseSchedule,
                     Resource,
                     Laptop,
                     Notification,
                     ScheduleEntry,
                     CourseScheduleEntry,
                     DAYS_OF_WEEK_CHOICES)

from .forms import ClientFileForm, ResourceForm, LaptopForm
from django.utils.html import format_html


class ClientFileInline(admin.TabularInline):
    model = ClientFile
    form = ClientFileForm
    extra = 0
    readonly_fields = ['file_link']

    def file_link(self, instance):
        return format_html("<a href='{}' target='_blank'>{}</a>", instance.file.url, instance.file.name)

    file_link.short_description = "File"


class ResourceInline(admin.TabularInline):
    model = Resource
    form = ResourceForm
    extra = 0


class CourseInline(admin.StackedInline):
    model = Course.clients.through  # This is the through model for the ManyToMany relationship
    extra = 1
    verbose_name = "Course Enrollment"
    verbose_name_plural = "Course Enrollments"


class ScheduleEntryInline(admin.StackedInline):
    model = ScheduleEntry
    fields = ('monday', 'monday_time_slot', 'tuesday', 'tuesday_time_slot',
              'wednesday', 'wednesday_time_slot', 'thursday', 'thursday_time_slot',
              'friday', 'friday_time_slot')
    extra = 0


class CourseScheduleEntryInline(admin.TabularInline):
    model = CourseScheduleEntry
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'start_date', 'end_date')
    inlines = [ScheduleEntryInline]
    filter_horizontal = ('clients',)


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = (
        'course_display',
        'monday_time_slot',
        'tuesday_time_slot',
        'wednesday_time_slot',
        'thursday_time_slot',
        'friday_time_slot'
    )

    fieldsets = (
        (None, {
            'fields': (('course',),
                       ('monday', 'monday_time_slot'),
                       ('tuesday', 'tuesday_time_slot'),
                       ('wednesday', 'wednesday_time_slot'),
                       ('thursday', 'thursday_time_slot'),
                       ('friday', 'friday_time_slot'))
        }),
    )

    def course_display(self, obj):
        return obj.course.name if obj.course else "No Course Assigned"

    course_display.short_description = "Course"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Check for conflicts after saving
        conflicts = self.check_for_conflicts(obj)

        # If conflicts were found, display a message in the admin interface
        if conflicts:
            message = f'Conflicts detected for {obj.course.name}: {", ".join(conflicts)}. Please resolve them.'
            messages.add_message(request, messages.ERROR, message)

    def check_for_conflicts(self, schedule_entry):
        # Get all other schedule entries for the same course that are not the current instance
        other_entries = ScheduleEntry.objects.filter(course=schedule_entry.course).exclude(pk=schedule_entry.pk)

        # Check each day for conflicts
        conflicts = []
        for day, _ in DAYS_OF_WEEK_CHOICES:
            if getattr(schedule_entry, day.lower()):
                time_slot = getattr(schedule_entry, f"{day.lower()}_time_slot")
                # Build a query to find other entries with the same day and time slot
                query = Q(**{f"{day.lower()}": True, f"{day.lower()}_time_slot": time_slot})
                if other_entries.filter(query).exists():
                    conflicts.append(f'{day} at {time_slot}')

        return conflicts


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFileInline, ResourceInline, CourseInline]

    list_display = ('name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement')
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement', 'assigned_laptop'),
        }),
    )


class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'get_schedule')

    def get_schedule(self, obj):
        days = obj.days.all()
        return ", ".join(day.name for day in days)

    get_schedule.short_description = "Schedule"


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'course', 'client')


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_to', 'period_start', 'period_end')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'created_at')
