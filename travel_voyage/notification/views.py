from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification, Booking
from .forms import NotificationForm
from django.db.models import Q
# Create your views here.

@login_required
def notification_list(request):
    # Get all bookings for the current user
    bookings = Booking.objects.filter(user=request.user)
    # Fetch notifications for the current user
    user_notifications = Notification.objects.filter(
        Q(user=request.user) | Q(user__in=bookings.values_list('accommodation__travel_id', flat=True))
    ).order_by('-created_at')

    # Fetch notifications sent by the travel agency for the user's bookings
    agency_notifications = Notification.objects.filter(
        user__in=bookings.values_list('accommodation__travel_id', flat=True)
    ).order_by('-created_at')

    return render(request, 'notification_list.html', {
        'user_notifications': user_notifications,
        # 'agency_notifications': agency_notifications
    })

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')  # Redirect back to the notification list

@login_required
def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect('add_notification')
    else:
        form = NotificationForm()
        notification = Notification.objects.filter(user=request.user)
    return render(request, 'add_notification.html', {'form': form, 'notifications': notification})



@login_required
def mark_agency_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('add_notification')  # Redirect back to the notifications list

        
        
