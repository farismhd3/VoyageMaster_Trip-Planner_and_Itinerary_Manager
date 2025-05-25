from django import forms
from django.utils import timezone
from .models import Trip, Itinerary, Activity

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destinations', 'start_date', 'end_date', 'budget']
        widgets = {
            'destinations': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")
        return end_date

from django import forms
from .models import Itinerary, Activity
from datetime import timedelta

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['day_number', 'activity']
        widgets = {
            'day_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super(ItineraryForm, self).__init__(*args, **kwargs)

        if self.trip:
            destination_ids = self.trip.destinations.values_list('id', flat=True)
            self.fields['activity'].queryset = Activity.objects.filter(destination__in=destination_ids)

    def clean_day_number(self):
        day_number = self.cleaned_data.get('day_number')
        if self.trip:
            trip_duration = (self.trip.end_date - self.trip.start_date).days + 1
            if day_number < 1 or day_number > trip_duration:
                raise forms.ValidationError(
                    f"Day number must be between 1 and {trip_duration} based on your trip duration."
                )
        return day_number
