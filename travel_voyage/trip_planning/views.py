from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.
from booking.models import Booking

@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trip_list.html', {'trips': trips})

@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()  # Save the trip instance first
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('/travel_agency_dashboard')  # Redirect to the trip list after creation
        
    else:
        form = TripForm()
    return render(request, 'trip_planning/manage_trip.html', {'t_form': form})

@login_required
def trip_edit(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trip_planning/trip_form.html', {'form': form})

@login_required
def trip_delete(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.delete()
    return redirect('/travel_agency_dashboard')

@login_required
def itinerary_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    itineraries = trip.itinerary_entries.all()
    form = ItineraryForm()
    return render(request, 'itinerary.html', {'trip': trip, 'itineraries': itineraries, 'form': form})


@login_required
def itinerary_create(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    if request.method == 'POST':
        form = ItineraryForm(request.POST, trip=trip)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.trip = trip
            itinerary.save()
            messages.success(request, "Itinerary entry added successfully.")
            return redirect('itinerary_list', trip_id=trip.id)
        else:
            messages.error(request, "There was an error adding the itinerary entry.")
            return redirect('itinerary_list', trip_id=trip.id)
    else:
        form = ItineraryForm(trip=trip)
    return render(request, 'itinerary.html', {'form': form, 'trip': trip})


@login_required
def itinerary_edit(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    if request.method == 'POST':
        form = ItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            return redirect('itinerary_list', trip_id=itinerary.trip.id)
    else:
        form = ItineraryForm(instance=itinerary)
    return render(request, 'itinerary.html', {'form': form, 'trip': itinerary.trip})

@login_required
def itinerary_delete(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    trip_id = itinerary.trip.id
    itinerary.delete()
    return redirect('itinerary_list', trip_id=trip_id)

@login_required
def get_activities(request, destination_id):
    activities = Activity.objects.filter(destination_id=destination_id).values('id', 'name')
    return JsonResponse({'activities': list(activities)})

@login_required
def package_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'u_vw_trip.html', {'trip': trip})

@login_required
def package_list(request):
    trips = Trip.objects.all()
    return render(request, 'package_list.html', {'trips': trips})

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    # Implement booking logic here (e.g., saving to a Booking model)
    messages.success(request, "Your trip has been booked successfully!")
    booking = Booking.objects.create(
        trip=trip,
        user=request.user,
        status='booked'
    )
    return redirect('/user_dashboard')  # Redirect to the trip list or another page


