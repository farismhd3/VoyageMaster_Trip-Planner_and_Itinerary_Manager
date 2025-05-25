from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import  *



urlpatterns = [
    path('',views.index),
    path('login',views.doLogin,name='login'),
    path('about/',views.about,name='about'),
    path('user_register', views.user_register, name='user_register'),
    path('traveller_register',views.traveller_register,name='traveller_register'),
    path('forgotpswd/',views.forgotpswd),
    path('logout/',views.logout),
    path('generate_random_password',views.generate_random_password),
    path('reset_password',views.reset_password,name='password_change'),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),


    path('destinations/', views.view_all_destinations, name='view_all_destinations'),
    path('activities/', views.view_all_activities, name='view_all_activities'),
    path('accommodations/', views.view_all_accommodations, name='view_all_accommodations'),


    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('activity/<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('accommodation/<int:accommodation_id>/', views.accommodation_detail, name='accommodation_detail'),
    

    path('set_availability', views.set_availability, name='set_availability'),

]
