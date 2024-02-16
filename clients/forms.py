#clients/forms.py

from django import forms
from .models import ClientFile, Resource, Laptop, Client, Course
from django.urls import reverse_lazy

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'
        widgets = {
            'seat_number': forms.Select(attrs={'class': 'custom-select'}),
            # Add other widgets as needed
        }

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['seat_number'].required = False  # Make seat_number optional


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'platform', 'start_date', 'end_date', 'clients']