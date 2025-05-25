from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from accomodation.models import Accommodation
from .forms import BookingForm
from user_app.models import Register
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models
from destination.models import Destination
from community.models import *
from django.db.models import Count
from notification.models import Notification

@login_required
def user_dashboard(request):
    today = timezone.now().date()
    accommodation_bookings = Booking.objects.filter(user=request.user, trip__isnull=True).order_by('-check_in')
    print(accommodation_bookings,"accommodation_bookings")
    trip_bookings = Booking.objects.filter(user=request.user, trip__isnull=False).order_by('-check_in')
    print(trip_bookings,"trip_bookings")
    discussions = Discussion.objects.filter(is_active=True).order_by('-created_at')
    user_discussions = discussions.filter(creator=request.user)
    posts = Post.objects.filter(author=request.user)
    total_discussions = discussions.count()
    user_discussions_count = user_discussions.count()
    user_posts_count = posts.count()
    popular_destinations = (
        Destination.objects.annotate(discussion_count=models.Count('discussion'))
        .order_by('-discussion_count')[:5]
    )
    context = {
        'accommodation_bookings': accommodation_bookings,
        'trip_bookings': trip_bookings,
        'discussions': discussions,
        'user_discussions': user_discussions,
        'posts': posts,
        'total_discussions': total_discussions,
        'user_discussions_count': user_discussions_count,
        'user_posts_count': user_posts_count,
        'popular_destinations': popular_destinations,
        'today': today
    }
    return render(request, 'u_dashboard.html', context)


@login_required
def booking_page(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    form = BookingForm()
    return render(request, 'reservation.html', {'accommodation': accommodation, 'form': form})

@login_required
def confirm_booking(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.accommodation = accommodation
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            total_price = (check_out - check_in).days * accommodation.price_per_night * booking.guests
            booking.total_price = total_price
            if check_in >= check_out:
                messages.error(request, 'Check-out date must be after check-in date.')
                return redirect('booking_page', accommodation_id=accommodation_id)

            booking.save()
            messages.success(request, 'Your booking has been confirmed!')
            
            Notification.objects.create(
                user=request.user,
                message='Your booking has been confirmed!',
                booking_id=booking.id
            )
            messages.success(request, 'Your booking has been confirmed!')
            return redirect('my_bookings') # Redirect to My Bookings after confirmation
        else:
            messages.error(request, 'There was an error with your booking.')
            return redirect('booking_page', accommodation_id=accommodation_id)

    return redirect('booking_page', accommodation_id=accommodation_id)




@login_required
def my_bookings(request):
    """Display a list of all bookings for the logged-in user."""
    today = timezone.now().date()
    accommodation_bookings = Booking.objects.filter(user=request.user, trip__isnull=True).order_by('-check_in')
    print(accommodation_bookings,"accommodation_bookings")
    trip_bookings = Booking.objects.filter(user=request.user, trip__isnull=False).order_by('-check_in')
    print(trip_bookings,"trip_bookings")
    return render(request, 'my_bookings.html', {
        'accommodation_bookings': accommodation_bookings,
        'trip_bookings': trip_bookings,
        'today': today
    })


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        Notification.objects.create(
            user=request.user,
            message='You have been cancelled your booking!',
            booking_id=booking.id
        )
        messages.success(request, 'Booking canceled successfully.')
        return redirect('my_bookings')
    return render(request, 'confirm_cancel.html', {'booking': booking})



@login_required
def agency_vw_bookings(request):
    bookings = Booking.objects.filter(accommodation__travel_id=request.user.id).order_by('-created_at')
    accommodation_bookings = Booking.objects.filter(user=request.user, trip__isnull=True).order_by('-check_in')
    trip_bookings = Booking.objects.filter(user=request.user, trip__isnull=False).order_by('-check_in')
    print(accommodation_bookings,"accommodation_bookings")
    print(trip_bookings,"trip_bookings,,,,,,,,,,,,,,")
    return render(request, 'agency_vw_bookings.html', {'bookings': bookings,'accommodation_bookings': accommodation_bookings,'trip_bookings': trip_bookings})






@login_required
def mark_as_completed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure that only the assigned guide can mark the booking as completed
    if booking.assigned_guide != request.user:
        messages.error(request, "You are not authorized to complete this booking.")
        return redirect('guide_bookings')

    # Check if the checkout date has passed
    if booking.is_past_checkout():
        # Mark the booking as completed
        booking.status = 'Completed'
        booking.save()

        # Send an email to the user confirming the completion of their booking
        send_mail(
            'Your Booking is Completed',
            f'Your booking at {booking.accommodation.name} is now completed.',
            'no-reply@yourwebsite.com',
            [booking.user.email],
            fail_silently=False,
        )

        messages.success(request, "Booking marked as completed and email sent to the user.")
    else:
        messages.error(request, "You cannot mark this booking as completed before the checkout date.")

    return redirect('guide_bookings')

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Process the payment here (integrate with your payment gateway)
        # For example, you might call a payment API and handle the response

        # If payment is successful
        booking.p_status = 'Paid'  # Update payment status
        booking.save()
        messages.success(request, 'Payment successful!')
        return redirect('my_bookings')

    return render(request, 'payment.html', {'booking': booking})


def recommendations_view(request):
    """Display a list of recommended destinations with their posts and comments."""
    recommendations = (
        Destination.objects.annotate(discussion_count=Count('discussion'))
        .order_by('-discussion_count')[:5]  # Top 5 by discussion count
    )
    print(recommendations,"recommendationsx")
    recommendations_with_posts = []

    for recommendation in recommendations:
        posts = Post.objects.filter(discussion__destination=recommendation).order_by('-created_at')
        post_bundles = []

        for post in posts:
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            post_bundles.append({
                'post': post,
                'comments': comments
            })

        recommendations_with_posts.append({
            'recommendation': recommendation,
            'posts': post_bundles
        })

    return render(request, 'recommendations.html', {
        'recommendations_with_posts': recommendations_with_posts,
    })