from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
# Create your views here.
def add_feedback_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user_id = request.user
            feedback.accommodation = accommodation
            feedback.save()
            return redirect('/accommodation_detail/', accommodation=accommodation.id)
    else:
        form = FeedbackForm()
    return render(request, 'add_feedback.html', {'form': form, 'accommodation': accommodation})

def add_feedback_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user_id = request.user
            feedback.activity = activity
            feedback.save()
            return redirect('activity_detail/', activity_id=activity.id)
    else:
        form = FeedbackForm()
    return render(request, 'add_feedback.html', {'form': form, 'activity': activity})