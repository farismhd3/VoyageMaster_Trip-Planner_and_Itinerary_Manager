from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Register(AbstractUser):
    usertype = models.IntegerField(default=0)
    phone = models.CharField(max_length=10,null=True, blank=True)
    place = models.CharField(max_length=300,null=True, blank=True)
    profile_image = models.FileField(upload_to='profile_images/', null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True) 
    location = models.CharField(max_length=200, null=True, blank=True)  
    latitude = models.FloatField(null=True, blank=True)  
    longitude = models.FloatField(null=True, blank=True) 
    experience = models.TextField(null=True, blank=True) 
    languages_spoken = models.CharField(max_length=200, null=True, blank=True)
    available = models.BooleanField(default=True)
    guide_license = models.CharField(max_length=100, null=True, blank=True)
    travel_id = models.CharField(max_length=100, null=True, blank=True)
    certifications = models.FileField(upload_to='certifications/', null=True, blank=True)
    is_approved = models.BooleanField(default=False) 
    status = models.CharField(max_length=50, default='pending')
    availability = models.CharField(max_length=20, default='available')  # Add this field