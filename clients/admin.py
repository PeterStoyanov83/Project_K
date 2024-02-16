# clients/admin.py
from django.contrib import admin
from .models import Client, ClientFile, Course, CourseSchedule, Resource, Laptop, Notification, ScheduleEntry, \
    CourseScheduleEntry
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
