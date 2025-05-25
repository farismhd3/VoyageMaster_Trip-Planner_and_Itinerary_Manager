from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.forms import modelformset_factory
# Create your views here.

@login_required
def add_accommodation(request):
    if request.method == "POST":
        accommodation_form = AccommodationForm(request.POST)
        images = request.FILES.getlist('images')  # Handle multiple image uploads

        if accommodation_form.is_valid():
            accommodation = accommodation_form.save(commit=False)
            accommodation.travel_id = Register.objects.get(id=request.user.id)
            accommodation.save()

            # Save each uploaded image
            for image in images:
                AccommodationImage.objects.create(accommodation=accommodation, image=image)

            messages.success(request, "Accommodation added successfully!")
        else:
            messages.error(request, "Failed to add accommodation. Please correct the errors.")

    return redirect('travel_agency_dashboard')

# Edit Accommodation View
def edit_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    if request.method == 'POST':
        accommodation_form = AccommodationForm(request.POST, request.FILES, instance=accommodation)
        if accommodation_form.is_valid():
            accommodation_form.save()

            # Handle New Image Uploads
            images = request.FILES.getlist('images')
            for image in images:
                AccommodationImage.objects.create(accommodation=accommodation, image=image)

            messages.success(request, 'Accommodation updated successfully!')
            return redirect('travel_agency_dashboard')  # Adjust the redirect URL as needed
    else:
        accommodation_form = AccommodationForm(instance=accommodation)

    return render(request, 'edit_accomodation.html', {'accommodation_form': accommodation_form, 'accommodation': accommodation})

# Delete Accommodation View
def delete_accommodation(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    accommodation.delete()
    messages.success(request, 'Accommodation deleted successfully!')
    return redirect('accommodation_list')  # Adjust the redirect URL as needed