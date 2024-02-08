from django import forms
from .models import Client, ClientFile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # Or list specific fields


class ClientFileForm(forms.ModelForm):
    DELETE_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]
    delete = forms.ChoiceField(choices=DELETE_CHOICES, required=False, widget=forms.RadioSelect, label='Delete')

    class Meta:
        model = ClientFile
        fields = ['file', 'delete']

    def __init__(self, *args, **kwargs):
        super(ClientFileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if the instance is already saved (i.e., has a primary key)
            self.fields['file'].widget = forms.HiddenInput()  # Hide the file input field
            self.initial['file'] = self.instance.file
            self.initial['delete'] = False  # Set initial value of delete to 'No'

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('delete', False)
        if delete and self.instance and self.instance.pk:
            self.instance.file.delete(save=False)  # Delete the file
        return cleaned_data
