from django import forms
from .models import Client, ClientFile


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # Or list specific fields


class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']
