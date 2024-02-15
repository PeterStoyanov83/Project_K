from django.contrib import admin
from clients.models import Client, ClientFile, Course, CourseSchedule, Resource, Laptop, Notification
from clients.forms import ClientFileForm, ResourceForm, LaptopForm
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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFileInline, ResourceInline, CourseInline]

    list_display = ('name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement', 'assigned_laptop')
    list_filter = ('location', 'date_of_entry', 'date_of_exit', 'signed_agreement')
    search_fields = ('name', 'location')
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement', 'assigned_laptop'),
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'start_date', 'end_date')
    list_filter = ('platform', 'start_date', 'end_date')
    search_fields = ('name',)
    filter_horizontal = ('clients',)


@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'get_schedule')

    def get_schedule(self, obj):
        days = obj.days.all()
        return ", ".join(day.name for day in days)

    get_schedule.short_description = "Schedule"


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'course', 'client')
    list_filter = ('course',)
    search_fields = ('seat_number', 'client__name')


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_to', 'period_start', 'period_end')
    list_filter = ('assigned_to', 'period_start', 'period_end')
    search_fields = ('name',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'created_at')
    list_filter = ('user', 'read', 'created_at')
    search_fields = ('message',)
