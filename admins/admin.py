from django.contrib import admin
from .models import Admin
from django.contrib.auth.models import Group, User

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # Adjust fields as needed
    # add more configurations as needed



# Unregister the default User and Group models.
admin.site.unregister(User)
admin.site.unregister(Group)