# clients/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Client, ClientFile, Course, CourseSchedule, Resource, Laptop
from .forms import ClientFileForm, ResourceForm, LaptopForm


# Inline classes allow editing of related records directly from the parent record's admin page.

# Inline class for CourseSchedule - allows editing of CourseSchedules from the Course admin page.
class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 0


# Inline class for ClientFile - allows editing of ClientFiles from the Client admin page.
class ClientFileInline(admin.TabularInline):
    model = ClientFile
    form = ClientFileForm
    fields = ['file']
    extra = 0


# Inline class for ClientCourse - allows editing of a Client's Courses from the Client admin page.
class ClientCourseInline(admin.TabularInline):
    model = Course.clients.through
    extra = 0


# Inline class for Resource - allows editing of Resources from the Course admin page.
class ResourceInline(admin.TabularInline):
    model = Resource
    form = ResourceForm
    extra = 0


# Inline class for Laptop - allows editing of Laptops from the Client admin page.
class LaptopInline(admin.TabularInline):
    model = Laptop
    form = LaptopForm
    extra = 0
    max_num = 1  # Allows only one laptop to be displayed in the inline.

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If there are already laptops assigned, do not allow adding more.
        self.max_num = 0 if qs.exists() else 1
        return qs

    def has_add_permission(self, request, obj=None):
        # Check if the client already has a laptop assigned.
        if obj:
            return not Laptop.objects.filter(assigned_to=obj).exists()
        return super().has_add_permission(request, obj)


# Admin class for Client
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientFileInline, ClientCourseInline, ResourceInline, LaptopInline]
    list_display = ['name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement']
    readonly_fields = ['courses_list']

    # This method is overridden to provide custom messages based on laptop availability.
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # The logic here should count if the number of unassigned laptops equals the total number of laptops
        total_laptops = Laptop.objects.count()
        unassigned_laptops = Laptop.objects.filter(assigned_to__isnull=True).count()

        if unassigned_laptops == 0:
            messages.warning(request, "No laptops available at the moment.")
        elif unassigned_laptops < total_laptops:
            messages.info(request, f"{unassigned_laptops} laptops available at the moment.")

        return super().change_view(request, object_id, form_url, extra_context)

    # This method provides a formatted list of courses in which the client is enrolled.
    def courses_list(self, obj):
        if obj.pk:  # If the client exists in the database
            courses = obj.enrolled_courses.all()
            links = [f"<a href='{reverse('admin:clients_course_change', args=[course.pk])}'>{course.name}</a>" for
                     course in courses]
            return format_html("<a href='{}'>Assign/Create Course</a>", reverse('admin:clients_course_add'))

    courses_list.short_description = "Enrolled Courses"


# Admin class for Course
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseScheduleInline, ResourceInline]
    list_display = ['name', 'platform', 'start_date', 'end_date', 'schedule_summary']
    filter_horizontal = ('clients',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['other_platform_comment'].disabled = False
        return form

    def schedule_summary(self, obj):
        schedules = obj.courseschedule_set.all()
        return ", ".join(f"{schedule.day_of_week} at {schedule.time_slot}" for schedule in schedules)

    schedule_summary.short_description = "Schedule"


# Admin class for ClientFile
class ClientFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'client', 'uploaded_at']
    list_select_related = ['client']


# Admin class for Laptop
class LaptopAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_to', 'period_start', 'period_end', 'comments']
    search_fields = ['name', 'assigned_to__name']
    list_filter = ['period_start', 'period_end']


# Registering the models with the admin site:
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientFile, ClientFileAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Resource)
admin.site.register(Laptop, LaptopAdmin)
