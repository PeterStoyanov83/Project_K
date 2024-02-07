from django.contrib import admin
from django import forms
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from .models import Client, ClientFile, Course, DayOfWeek, TimeSlot


# Assuming ClientFileForm is correctly defined elsewhere if needed.

class ClientAdminForm(forms.ModelForm):
    new_file = forms.FileField(required=False, label='Upload New File')
    # This field will collect the IDs of files to delete.
    files_to_delete = forms.ModelMultipleChoiceField(
        queryset=ClientFile.objects.none(), required=False,
        widget=forms.CheckboxSelectMultiple, label='Mark files for deletion'
    )

    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['files_to_delete'].queryset = self.instance.files.all()


class ClientAdminForm(forms.ModelForm):
    new_file = forms.FileField(required=False, label='Upload New File')

    # No need for an inline field for deletion, we will handle deletion through actions
    # in the ClientAdmin class

    class Meta:
        model = Client
        fields = '__all__'


class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    # No inlines for ClientFile, handle it through readonly_fields and actions
    readonly_fields = ['uploaded_files']

    def uploaded_files(self, instance):
        files_html = format_html_join(
            mark_safe('<br>'),
            "<a href='{}' target='_blank'>{}</a>",
            ((f.file.url, f.file.name.split('/')[-1]) for f in instance.files.all())  # Split to get only the file name
        )
        return files_html or 'No files uploaded.'

    uploaded_files.short_description = "Uploaded Files"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handling the new file upload
        if 'new_file' in form.cleaned_data and form.cleaned_data['new_file']:
            new_file = form.cleaned_data['new_file']
            client_file = ClientFile(file=new_file)
            client_file.save()
            obj.files.add(client_file)

    # We will use the 'actions' feature of the admin to allow deletion of files
    actions = ['delete_selected_files']

    def delete_selected_files(self, request, queryset):
        # Custom action to delete selected files
        for obj in queryset:
            obj.files.clear()  # This will remove the relationship to the files without deleting the files themselves

    delete_selected_files.short_description = "Delete selected files from the client"


# ... Your existing CourseAdmin, DayOfWeekAdmin, TimeSlotAdmin ...

class ClientFileAdmin(admin.ModelAdmin):
    list_display = ('file_link', 'uploaded_at')
    search_fields = ('file',)

    def file_link(self, obj):
        return mark_safe(f"<a href='{obj.file.url}' target='_blank'>{obj.file.name.split('/')[-1]}</a>")

    file_link.short_description = 'File'

    # Optionally, you can override the 'get_queryset' method to limit the files to those related to a Client.
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(clients__isnull=False)


# Register other model admins as needed
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientFile)
admin.site.register(Course)
admin.site.register(DayOfWeek)
admin.site.register(TimeSlot)
