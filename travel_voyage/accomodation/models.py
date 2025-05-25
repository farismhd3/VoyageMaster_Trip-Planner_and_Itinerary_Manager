from django.db import models
from destination.models import Destination
# Create your models here.
from user_app.models import Register



class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="accommodations")
    address = models.CharField(max_length=200)
    price_per_night = models.FloatField(null=True)
    amenities = models.TextField(null=True, blank=True)  # Example: "Wi-Fi, Breakfast, Pool"
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    travel_id = models.ForeignKey(Register,max_length=100, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="accommodation_images/")

    def __str__(self):
        return f"Image for {self.accommodation.name}"
