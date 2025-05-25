from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    guests = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests...'})
    )
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'special_requests']
 