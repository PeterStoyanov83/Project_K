# clients/forms.py

from django import forms
from django.core.exceptions import ValidationError

from .models import Client, ClientFile, Resource, Laptop


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # Or list specific fields


class ClientFileForm(forms.ModelForm):
    DELETE_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]

    class Meta:
        model = ClientFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(ClientFileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
            self.fields['file'].widget = forms.HiddenInput()  # Hide the file input field
            self.initial['file'] = self.instance.file

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('delete', False)
        if delete and self.instance and self.instance.pk:
            self.instance.file.delete(save=False)  # Delete the file
        return cleaned_data


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['seat_number'].queryset = self.get_seat_queryset()

    def get_seat_queryset(self):
        # Adjust the queryset based on room and current assignments
        if self.instance.room == 'room_1':
            taken_seats = Resource.objects.filter(
                room='room_1',
                course=self.instance.course).values_list(
                'seat_number',
                flat=True
            )
            return range(1, 9)  # Assuming seat numbers are 1 through 8
        elif self.instance.room == 'room_2':
            taken_seats = Resource.objects.filter(
                room='room_2',
                course=self.instance.course).values_list(
                'seat_number',
                flat=True
            )
            return range(1, 5)  # Assuming seat numbers are 1 through 4
        else:
            return range(1, 9)  # Default range if room not set


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['name', 'assigned_to', 'period_start', 'period_end', 'comments']

    def __init__(self, *args, **kwargs):
        super(LaptopForm, self).__init__(*args, **kwargs)
        # Initialize any dynamic choices or set initial values as needed
        # For instance, to include only unassigned laptops:
        # self.fields['name'].queryset = Laptop.objects.filter(assigned_to__isnull=True)

        # If 'name' is a CharField and you have a set list of names:
        LAPTOP_NAMES = [
            ('laptop1', 'Laptop 1'),
            ('laptop2', 'Laptop 2'),
            ('laptop3', 'Laptop 3'),
            ('laptop4', 'Laptop 4')
        ]

        self.fields['name'].choices = LAPTOP_NAMES

        # Set initial values or adjust queryset for 'assigned_to' if needed
        # For example, to exclude clients who already have a laptop assigned:
        self.fields['assigned_to'].queryset = Client.objects.filter(assigned_laptops__isnull=True)

        # You can also set up widgets if you want to customize the appearance of the input fields:
        self.fields['period_start'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['period_end'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['comments'].widget = forms.Textarea(attrs={'rows': 3, 'cols': 40})

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        assigned_to = cleaned_data.get('assigned_to')

        # Check if the laptop is already assigned
        if name:
            try:
                laptop = Laptop.objects.get(name=name)
                if laptop.assigned_to and laptop.assigned_to != assigned_to:
                    # Add an error to the 'name' field specifically
                    self.add_error('name', f"Laptop '{name}' is already assigned to {laptop.assigned_to.name}")
            except Laptop.DoesNotExist:
                # If the laptop doesn't exist, there's no conflict
                pass
        # Ensure the period end date is not before the period start date
        period_start = cleaned_data.get('period_start')
        period_end = cleaned_data.get('period_end')
        if period_end and period_start and period_end < period_start:
            self.add_error('period_end', "The end date cannot be before the start date.")

        return cleaned_data
