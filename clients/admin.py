from django.contrib import admin
from .models import Client, ClientFile, Course, CourseSchedule
from django import forms
from .forms import ClientFileForm
from django.utils.html import format_html
from django.urls import reverse


class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 0


class ClientFileForm(forms.ModelForm):
    delete = forms.BooleanField(
        required=False,  # Make the field optional
        widget=forms.CheckboxInput(attrs={'class': 'delete-checkbox'}),
        # Use a checkbox widget with a custom class for styling if needed
        label='Delete'  # The label next to the checkbox
    )

    class Meta:
        model = ClientFile
        fields = ['file', 'delete']

    def __init__(self, *args, **kwargs):
        super(ClientFileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
            # self.fields['file'].widget = forms.HiddenInput()  # Hide the file input field
            self.initial['delete'] = False  # Set initial value of delete to False

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('delete', False)
        if delete and self.instance and self.instance.pk:
            self.instance.file.delete(save=False)  # Delete the file
        return cleaned_data


# Inline class for ClientFile
class ClientFileInline(admin.TabularInline):
    model = ClientFile
    form = ClientFileForm
    extra = 0  # Number of extra blank forms

    def get_fields(self, request, obj=None):
        if obj:
            # obj will be None on the add page, and an instance on the change page
            return ['file', 'delete']
        else:
            return ['file']

    def get_readonly_fields(self, request, obj=None):
        # Make file readonly when it's already uploaded
        if obj:
            return ['file']
        return []


# Admin for ClientFile, if you want to manage it separately as well
class ClientFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'client', 'uploaded_at']
    list_select_related = ['client']


# Form for ClientAdmin, to specify which fields to include
class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


# Admin for Client, now with ClientFile inline
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    inlines = [ClientFileInline, ]
    list_display = ['name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement']
    readonly_fields = ['courses_list', ]  # Add this to your existing readonly_fields if you have any

    # Method to display the courses on the client change page
    def courses_list(self, obj):
        if obj.pk:  # checks if the client object exists
            courses = obj.enrolled_courses.all()
            if courses:
                links = [
                    f"<a href='{reverse('admin:clients_course_change', args=[course.pk])}'>{course.name}</a>"
                    for course in courses
                ]
                return format_html("<ul>" + "".join(f"<li>{link}</li>" for link in links) + "</ul>")
        return "No courses enrolled"
    courses_list.short_description = "Enrolled Courses"


# Admin for Course
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseScheduleInline, ]

    # Remove 'days_of_week' and 'time_slot' from list_display
    list_display = ['name', 'platform', 'start_date', 'end_date']
    filter_horizontal = ('clients',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseAdmin, self).get_form(request, obj, **kwargs)

        form.base_fields['other_platform_comment'].disabled = False
        return form

    # Optionally, you can add a method to display a summary of the schedules
    def schedule_summary(self, obj):
        schedules = CourseSchedule.objects.filter(course=obj)
        return ", ".join(f"{schedule.day_of_week} at {schedule.time_slot}" for schedule in schedules)

    schedule_summary.short_description = "Schedule"

    # Add the new method to list_display if you want to show the schedules in the admin list view
    list_display.append('schedule_summary')


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientFile, ClientFileAdmin)
admin.site.register(Course, CourseAdmin)
