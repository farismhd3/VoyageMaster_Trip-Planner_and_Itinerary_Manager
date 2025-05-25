from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_app.models import Register
from .forms import *
from accomodation.models import *
from accomodation.forms import *
from destination.forms import *
from .models import *
from booking.models import *
from community.models import Discussion, Post
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from trip_planning.models import *
from trip_planning.forms import *
import logging

logger = logging.getLogger(__name__)

@login_required
def travel_agency_dashboard(request):
    if request.session.get('ut') != 2:  # Ensure user is a travel agency
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    user = request.user
    # Fetch data
    
    destinations = Destination.objects.filter(travel_id=request.user.id)
    activities = Activity.objects.filter(destination__travel_id=request.user.id)
    accommodations = Accommodation.objects.filter(travel_id=request.user.id)  # Fetch accommodations
    accommodation_form = AccommodationForm() 
    destination_form = DestinationForm()
    activity_form = ActivityForm()
    bookings = Booking.objects.filter(accommodation__travel_id=request.user.id).order_by('-created_at')
    booking = Booking.objects.filter(accommodation__travel_id=request.user.id).order_by('-created_at')
    discussions = Discussion.objects.filter(is_active=True).order_by('-created_at')
    t_destinations = Destination.objects.all()
    user_discussions = discussions.filter(creator=user)
    posts = Post.objects.filter(author=user)
    total_discussions = discussions.count()
    user_discussions_count = user_discussions.count()
    user_posts_count = posts.count()
    # accommodations = Accommodation.objects.filter(travel_id=request.user)  # Filter by the agency user
    print(accommodations)
    # Fetch bookings related to those accommodations
    bookings = Booking.objects.filter(accommodation__in=accommodations)  # Only include bookings with agency accommodations

    # Get available years for filtering
    available_years = bookings.dates('check_in', 'year').distinct()  # Get distinct years from bookings

    # Calculate total expenses
    
    # Group by month for detailed analysis
    selected_year = request.GET.get('year', None)
    if selected_year:
        bookings = bookings.filter(check_in__year=selected_year)  # Filter bookings by selected year
    total_expense = sum(booking.total_price for booking in bookings)  # Calculate total expenses
    total_expense = float(total_expense)
    # Group by month for detailed analysis
    monthly_expenses = (
        bookings
        .annotate(month=TruncMonth('check_in'))  # Group by month of check-in
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )

    # Prepare data for the chart
    months = []
    expenses = []
    for entry in monthly_expenses:
        months.append(entry['month'].strftime('%B %Y'))  # Format month
        expenses.append(float(entry['total']))  # Ensure this is a float

    # Get available years for filtering
    available_years = booking.dates('check_in', 'year').distinct()  # Get distinct years from bookings


    # Prepare data for the chart
    months = []
    expenses = []
    for entry in monthly_expenses:
        months.append(entry['month'].strftime('%B %Y'))  # Format month
        expenses.append(entry['total'])

    # Optional: Popular destinations logic
    popular_destinations = (
        Destination.objects.annotate(discussion_count=models.Count('discussion'))
        .order_by('-discussion_count')[:5]
    )
    expenses = [float(entry['total']) for entry in monthly_expenses]
    t_form=TripForm()
    trips = Trip.objects.filter(user=request.user)
    accommodation_bookings = Booking.objects.filter(user=request.user, trip__isnull=True).order_by('-check_in')
    trip_bookings = Booking.objects.filter(trip__user=request.user, trip__isnull=False).order_by('-check_in')
    context = { 
        'bookings': bookings,
        'accommodation_bookings': accommodation_bookings,
        'trip_bookings': trip_bookings,
        'total_expense': total_expense,
        'destinations': destinations,
        'activities': activities,
        'accommodations': accommodations,
        'destination_form': destination_form,
        'activity_form': activity_form,
        'accommodation_form':accommodation_form,
        'bookings': bookings,
        'discussions': discussions,  # ✅ Add this
        't_destinations': t_destinations,
        'total_discussions': total_discussions,
        'user_discussions_count': user_discussions_count,
        'user_posts_count': user_posts_count,
        'popular_destinations': popular_destinations,
        'monthly_expenses': monthly_expenses,
        'months': months,
        'expenses': expenses,
        'available_years': available_years,
        'selected_year': selected_year,
        't_form':t_form,
        'trips':trips,
    }
    logger.debug("Context: %s", context) 
    return render(request, 'travel_agency_dashboard.html', context)


@login_required
def add_activity(request):
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity added successfully!")
        else:
            messages.error(request, "Failed to add activity. Please correct the errors.")
    return redirect('travel_agency_dashboard')



@login_required
def edit_activity(request, activity_id):
    # Fetch the activity to edit, ensuring it belongs to the current travel agency
    activity = get_object_or_404(Activity, id=activity_id, destination__travel_id=request.user.id)

    if request.method == "POST":
        # Bind POST data to the existing activity instance
        edit_activity_form = ActivityForm(request.POST, request.FILES, instance=activity)
        if edit_activity_form.is_valid():
            # Save the updated activity
            edit_activity_form.save()
            messages.success(request, "Activity updated successfully.")
            return redirect('travel_agency_dashboard')
        else:
            messages.error(request, "Failed to update activity. Please correct the errors.")
    else:
        # Initialize the form with the current activity data
        edit_activity_form = ActivityForm(instance=activity)

    return render(request, 'edit_activity.html', {'edit_activity_form': edit_activity_form})



@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, destination__travel_id=request.user.id)
    activity.delete()
    messages.success(request, "Activity deleted successfully.")
    return redirect('travel_agency_dashboard')

@login_required
def agency_community(request):
    # Get recent discussions
    discussions = Discussion.objects.filter(is_active=True).order_by('-created_at')[:10]
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user)
    
    # Get user's discussions
    user_discussions = Discussion.objects.filter(creator=request.user)
    
    # Get popular destinations based on discussion count
    popular_destinations = Destination.objects.annotate(
        discussion_count=Count('discussion')
    ).order_by('-discussion_count')[:5]
    
    context = {
        'discussions': discussions,
        'posts': user_posts,
        'user_discussions': user_discussions,
        'popular_destinations': popular_destinations,
        'total_discussions': discussions.count(),
        'user_discussions_count': user_discussions.count(),
        'user_posts_count': user_posts.count(),
    }
    
    return render(request, 'community/agency_community.html', context)



@login_required
def agency_expense_tracker(request):
    # Fetch all accommodations related to the logged-in agency
    accommodations = Accommodation.objects.filter(travel_id=request.user)  # Filter by the agency user

    # Fetch bookings related to those accommodations
    bookings = Booking.objects.filter(accommodation__in=accommodations)  # Only include bookings with agency accommodations
    booking = Booking.objects.filter(accommodation__in=accommodations)  # Only include bookings with agency accommodations

    # Calculate total expenses
    total_expense = sum(booking.total_price for booking in bookings)  # Calculate total expenses

    # Group by month for detailed analysis
    monthly_expenses = (
        bookings
        .annotate(month=TruncMonth('check_in'))  # Group by month of check-in
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )
    selected_year = request.GET.get('year', None)
    if selected_year:
        bookings = bookings.filter(check_in__year=selected_year)  # Filter bookings by selected year

    # Prepare data for the chart
    months = []
    expenses = []
    for entry in monthly_expenses:
        months.append(entry['month'].strftime('%B %Y'))  # Format month
        expenses.append(float(entry['total']))  # Ensure this is a float

    print("Months:", months)  # Debugging output
    print("Expenses:", expenses)  # Debugging output
    available_years = booking.dates('check_in', 'year').distinct()
    return render(request, 'expense.html', {
        'bookings': bookings,
        'total_expense': total_expense,
        'months': months,
        'expenses': expenses,
        'available_years': available_years,
    })