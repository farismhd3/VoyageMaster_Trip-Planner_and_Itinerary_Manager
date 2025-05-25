from django.contrib import messages
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from . models import *
from .forms import *
from notification.models import Notification
from  django.core.files.storage import FileSystemStorage
import os
from accomodation.models import *
from destination.models import *
from agency_app.models import *
import secrets
import string
from booking.models import Booking
from django.db.models import Q

def index(request):
    user=request.user
    destinations = Destination.objects.all()[:3]
    activities = Activity.objects.prefetch_related('activity_feedbacks').all()[:3]  # Corrected related name
    accommodations = Accommodation.objects.prefetch_related('accommodation_feedbacks', 'images').all()[:3]  # Corrected related name
    bookings=[]
    unread_count=0
    if user.is_authenticated:
        bookings=Booking.objects.filter(user=request.user)
        unread_count = Notification.objects.filter(
            Q(user=request.user) |  # Notifications for the current user
            # Notifications related to bookings made by the current user
            Q(user__in=bookings.values_list('accommodation__travel_id', flat=True))  # Notifications sent by the travel agency for the user's bookings
        ).filter(is_read=False).count()
    context = {
        'destinations': destinations,
        'activities': activities,
        'accommodations': accommodations,
        'unread_count': unread_count,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request,'about.html')
def doLogin(request):
    form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, 'Username and password are required.', extra_tags='log')
            return render(request, 'login.html', {'form': form})

        user = authenticate(request, username=username, password=password)
        if user is None:
            if not Register.objects.filter(username=username).exists():
                messages.error(request, 'Invalid username.', extra_tags='reg')
            else:
                messages.error(request, 'Invalid password.', extra_tags='reg')
            return render(request, 'login.html', {'form': form})

        # If the user is authenticated, check if they are a superuser
        if user.is_superuser:
            # Ensure the Register entry is updated to reflect admin rights
            register_entry, created = Register.objects.get_or_create(username=user.username, defaults={'usertype': 1})
            if not created and register_entry.usertype != 1:  # Update existing record
                register_entry.usertype = 1
                register_entry.is_approved = True
                register_entry.save()

        # Perform login
        login(request, user)

        # Fetch user data from the Register table
        data = Register.objects.get(username=user.username)
        request.session['ut'] = data.usertype
        request.session['uid'] = data.id

        # Display login success message
        messages.success(request, f'Login Successful! Welcome {data.username}.', extra_tags='log')
        return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/') 

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Register.objects.filter(email=email).exists():
                login_form = LoginForm()  
                return render(request, 'login.html', {'form': login_form, 'z': True})
            else:
                try:
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.usertype = 0
                    user.is_approved = True
                    user.is_active=True
                    user.status="approved"
                    user.save()
                    messages.success(request, f'Your registration has been successful! You can login now.', extra_tags='log')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
        title='User'
    return render(request, 'register.html', {'form': form,'title':title})



def traveller_register(request):
    if request.method == 'POST':
        form = TravelAgencyRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Register.objects.filter(email=email).exists():
                login_form = LoginForm()  
                return render(request, 'login.html', {'form': login_form, 'z': True})
            else:
                try:
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.usertype = 2
                    user.is_approved = False
                    user.is_active=False
                    user.save()
                    messages.success(request, 'Your registration has been successful! You can login only after admin approval.', extra_tags='log_dr')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        return render(request, 'register.html', {'form': form,'title':'Driver'})
    else:
        form = TravelAgencyRegisterForm()
        title='Travel Agency'
    return render(request, 'register.html', {'form': form,'title':title})

def forgotpswd(request):
    return render(request, 'forgotpswd.html', {'user': request.user})

def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def reset_password(request):
    if request.method == "POST":

                user = Register.objects.get(username=request.POST['username'])
                print("USERSS",user)
                new_password = generate_random_password()
                user.password = make_password(new_password)
                print('Nesw Passworddddddddd',new_password)
                user.save()
                subject = 'password'
                message = "your password is " + str(new_password)
                email_from = settings.EMAIL_HOST_USER
                recepient_list = [user.email]  
                send_mail(subject,message,email_from,recepient_list)
                messages.success(request, f'New Password is send to your registered email. Use it for login and change your password in your profile section. ', extra_tags='log')
               
    else:
        return render(request,"forgotpswd.html")
    return redirect('/login')

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email is already in use by another user
            if Register.objects.filter(email=email).exclude(id=request.user.id).exists():
                form.add_error('email', 'Email already exists')
            else:
                try:
                    user = form.save(commit=False)
                    if form.cleaned_data.get('password'):
                        user.password = make_password(form.cleaned_data['password'])
                    user.save()

                    # Update the session with the new user data
                    update_session_auth_hash(request, user)

                    messages.success(request, 'Profile updated successfully.',extra_tags='log')
                    return redirect('/profile')
                except Exception as e:
                    form.add_error(None, f'An error occurred while updating the profile: {e}')
        else:
            messages.error(request, 'Please correct the errors below.', extra_tags='log')
    else:
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'place': request.user.place,
            'phone': request.user.phone,
            'image': request.user.image
        }
        form = ProfileForm(initial=initial_data, instance=request.user)
    
    return render(request, 'update_form.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        print("POST request received.")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("Form is valid.")
            try:
                user = form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, 'Your password has been changed successfully.', extra_tags='log')
                return redirect('/login')
            except Exception as e:
                print(f"Error saving form: {e}")
                messages.error(request, 'An error occurred. Please try again.', extra_tags='log')
        else:
            # Debugging: print form errors
            print("Form is not valid.")
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the error below.', extra_tags='log')
    else:
        print("GET request received.")
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'password_change_form.html', {'form': form})






def view_all_destinations(request):
    # Get all destinations
    destinations = Destination.objects.all()
    context = {'destinations': destinations, 'title': 'All Destinations'}
    return render(request, 'view_all.html', context)

def view_all_activities(request):
    # Get all activities
    activities = Activity.objects.all()
    context = {'activities': activities, 'title': 'All Activities'}
    return render(request, 'view_all.html', context)

def view_all_accommodations(request):
    # Get all accommodations
    accommodations = Accommodation.objects.prefetch_related('images').all()
    context = {'accommodations': accommodations, 'title': 'All Accommodations'}
    return render(request, 'view_all.html', context)





def destination_detail(request, destination_id):
    # Get the selected destination
    destination = get_object_or_404(Destination, id=destination_id)

    # Get related activities and accommodations
    activities = destination.activities.all()
    accommodations = destination.accommodations.all()

    context = {
        'destination': destination,
        'activities': activities,
        'accommodations': accommodations,
    }
    return render(request, 'destination_detail.html', context)


def activity_detail(request, activity_id):
    # Get the selected activity
    activity = get_object_or_404(Activity, id=activity_id)

    # Get related destination and accommodations
    destination = activity.destination
    accommodations = destination.accommodations.all()

    context = {
        'activity': activity,
        'destination': destination,
        'accommodations': accommodations,
    }
    return render(request, 'activity_detail.html', context)


def accommodation_detail(request, accommodation_id):
    # Fetch the specific accommodation
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    # Get the related destination and activities
    destination = accommodation.destination
    activities = destination.activities.all()

    context = {
        'accommodation': accommodation,
        'destination': destination,
        'activities': activities,
    }
    return render(request, 'accommodation_detail.html', context)




@login_required
def set_availability(request):
    if request.method == 'POST':
        availability = request.POST.get('availability')
        guide = Register.objects.get(id=request.user.id)
        guide.availability = availability
        guide.save()
        messages.success(request, 'Availability updated successfully!', extra_tags='log')
        return redirect('/')
    else:
        guide = Register.objects.get(id=request.user.id)
        return render(request, 'availability.html', {'guide': guide})