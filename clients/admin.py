from django.contrib import admin
from .models import Client, Course


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    list_filter = ['location']  # Optionally add filters
    search_fields = ['name']  # Optionally enable search by client name


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'client_count']

    def client_count(self, obj):
        # Replace 'clients' with the related_name of the many-to-many field in your Course model
        return obj.clients.count()

    client_count.short_description = 'Number of Clients'
