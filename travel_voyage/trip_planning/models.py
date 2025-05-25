from django.db import models
from django.contrib.auth.models import User
from user_app.models import Register
from destination.models import Destination
from agency_app.models import Activity

class Trip(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    destinations = models.ManyToManyField(Destination)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip by {self.user} - {self.start_date} to {self.end_date}"

class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itinerary_entries')
    day_number = models.IntegerField()
    activity = models.ManyToManyField(Activity)
    location = models.CharField(max_length=100, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Itinerary for {self.trip} - Day {self.day_number}"
