from django.db import models
from user_app.models import Register
from accomodation.models import Accommodation
# Create your models here.
from trip_planning.models import Trip

class Booking(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True,blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE,null=True,blank=True)
    check_in = models.DateField(null=True,blank=True)
    check_out = models.DateField(null=True,blank=True)
    guests = models.IntegerField(null=True,blank=True)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    p_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending',null=True,blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending',null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,null=True,blank=True)
    