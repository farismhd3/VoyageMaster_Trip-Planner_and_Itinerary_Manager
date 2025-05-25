from django.db import models

from user_app.models import Register

# Create your models here.
class Destination(models.Model):
    place = models.CharField(max_length=100)
    description = models.TextField()
    travel_id = models.ForeignKey(Register,max_length=100, null=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destination_images/', null=True, blank=True)
    def __str__(self):
        return self.place