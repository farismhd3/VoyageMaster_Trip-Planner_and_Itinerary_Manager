from django import forms
from user_app.models import Register
from .models import *





class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['place', 'description','image']
        widgets = {
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }