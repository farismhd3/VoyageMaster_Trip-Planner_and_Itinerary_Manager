from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment_view'),  # Add this line
    path('agency_vw_bookings', views.agency_vw_bookings, name='agency_vw_bookings'),
    path('booking/<int:accommodation_id>/', views.booking_page, name='booking_page'),
    path('confirm-booking/<int:accommodation_id>/', views.confirm_booking, name='confirm_booking'),
    path('recommendations', views.recommendations_view, name='recommendations'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),


    
    
    path('guide_booking/<int:booking_id>/complete/', views.mark_as_completed, name='mark_as_completed'),

]
