from django import forms
from user_app.models import Register
from .models import *
from django.core.exceptions import ValidationError
import re






class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['destination', 'spot_name', 'description', 'image', 'opening_time', 'closing_time', 'entry_fee', 'place', 'exact_location']
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'spot_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity Spot Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'entry_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entry Fee'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'}),
            'exact_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exact Location'}),
        }