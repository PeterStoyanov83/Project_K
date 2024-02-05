# admin.py of your clients app

from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Client
from django.shortcuts import get_object_or_404, render


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'signed_agreement',
        'view_files_link'
    )

    def view_files_link(self, obj):
        return format_html(
            '<a href="{}">View Files</a>',
            reverse('admin:client_files',
                    args=[obj.pk]))

    view_files_link.short_description = 'Files'

    def edit_link(self, obj):
        return format_html(
            '<a href="{}">Edit</a>',
            reverse('admin:clients_client_change',
                    args=[obj.pk]))

    edit_link.short_description = 'Edit Client'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/files/', self.admin_site.admin_view(self.view_files), name='client_files'),
        ]
        return custom_urls + urls

    def view_files(self, request, object_id):
        client = get_object_or_404(Client, pk=object_id)

        return render(request, 'admin/view_files.html', {'client': client})

    view_files_link.short_description = 'Files'

