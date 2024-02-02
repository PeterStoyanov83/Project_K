from django.contrib import admin
from django.db.models import Count  # Import Count function
from .models import Client, Course, ClientFile


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'signed_agreement_column', 'list_files')
    readonly_fields = ('name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement', 'files')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(courses_count=Count('courses'))  # Use Count function
        return queryset

    def signed_agreement_column(self, obj):
        return "Yes" if obj.signed_agreement else "No"

    signed_agreement_column.short_description = 'Signed Agreement'

    def list_files(self, obj):
        return ', '.join([file.file_type for file in obj.files.all()])

    list_files.short_description = 'Files'

    def courses_count(self, obj):
        return obj.courses_count

    courses_count.short_description = 'Number of Courses'
    change_form_template = 'clients/client_profile.html'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'client_count')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(client_count=Count('clients'))  # Use Count function
        return queryset

    def client_count(self, obj):
        return obj.client_count

    client_count.short_description = 'Number of Clients'
