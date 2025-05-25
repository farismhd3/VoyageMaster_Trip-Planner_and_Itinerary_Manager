from django import forms
from .models import Accommodation, AccommodationImage

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'destination', 'address', 'price_per_night', 'amenities', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Accommodation Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price Per Night'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Amenities'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }


class AccommodationImageForm(forms.ModelForm):
    class Meta:
        model = AccommodationImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
