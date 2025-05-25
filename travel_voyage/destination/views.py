from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_app.models import Register
from .forms import *
from .models import *

# Create your views here.

@login_required
def add_destination(request):
    if request.method == "POST":
        form = DestinationForm(request.POST,request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.travel_id = Register.objects.get(id=request.user.id)
            destination.save()
            messages.success(request, "Destination added successfully!")
        else:
            messages.error(request, "Failed to add destination. Please correct the errors.")
    return redirect('travel_agency_dashboard')



@login_required
def edit_destination(request, destination_id):
    # Fetch the destination to edit, ensuring it belongs to the current travel agency
    destination = get_object_or_404(Destination, id=destination_id, travel_id=request.user.id)

    if request.method == "POST":
        # Bind POST data to the existing destination instance
        edit_destination_form = DestinationForm(request.POST,request.FILES, instance=destination)
        if edit_destination_form.is_valid():
            # Save the updated destination
            edit_destination_form.save()
            messages.success(request, "Destination updated successfully.")
            return redirect('travel_agency_dashboard')
        else:
            messages.error(request, "Failed to update destination. Please correct the errors.")
    else:
        # Initialize the form with the current destination data
        edit_destination_form = DestinationForm(instance=destination)

    return render(request, 'edit_destination.html', {'edit_destination_form': edit_destination_form})


@login_required
def delete_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, travel_id=request.user.id)
    destination.delete()
    messages.success(request, "Destination deleted successfully.")
    return redirect('travel_agency_dashboard')
