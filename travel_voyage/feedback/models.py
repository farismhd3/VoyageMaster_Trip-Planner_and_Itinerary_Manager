from django.db import models

from user_app.models import *
from accomodation.models import *
from agency_app.models import *

# Create your models here.
class Feedback(models.Model):
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, related_name="feedbacks")
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True, blank=True, related_name="accommodation_feedbacks")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True, related_name="activity_feedbacks")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=0)  # Ratings from 1 to 5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.accommodation:
            return f"Feedback for Accommodation: {self.accommodation.name} by {self.user_id.username}"
        if self.activity:
            return f"Feedback for Activity: {self.activity.spot_name} by {self.user_id.username}"
        return f"Feedback by {self.user_id.username}"
