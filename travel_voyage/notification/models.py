from django.db import models
from django.contrib.auth.models import User
from booking.models import Booking
from user_app.models import Register
from trip_planning.models import Trip
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    message = models.TextField()
    booking_id = models.IntegerField(null=True, blank=True)  # Optional, if related to a booking
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)  # Optional, if related to a trip
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
