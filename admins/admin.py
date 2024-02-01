from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # Adjust fields as needed
    # add more configurations as needed
