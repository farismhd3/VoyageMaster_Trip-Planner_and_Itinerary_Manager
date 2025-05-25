from django.db import models
from user_app.models import *
from destination.models import Destination
class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="activities")
    spot_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image=models.FileField(upload_to='activity_images/', null=True, blank=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    entry_fee = models.FloatField(null= True)
    place = models.CharField(max_length=100)
    exact_location = models.CharField(max_length=200)
    travel_id = models.ForeignKey(Register,max_length=100, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.spot_name + " - " + self.destination.place

