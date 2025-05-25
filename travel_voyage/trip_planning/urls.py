from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_list, name='trip_list'),
    path('create/', trip_create, name='trip_create'),
    path('edit/<int:trip_id>/', trip_edit, name='trip_edit'),
    path('delete/<int:trip_id>/', trip_delete, name='trip_delete'),
    path('itinerary/<int:trip_id>/', itinerary_list, name='itinerary_list'),
    path('itinerary/create/<int:trip_id>/', itinerary_create, name='itinerary_create'),
    path('itinerary/edit/<int:itinerary_id>/', itinerary_edit, name='itinerary_edit'),
    path('itinerary/delete/<int:itinerary_id>/', itinerary_delete, name='itinerary_delete'),
    path('get_activities/<int:destination_id>/', get_activities, name='get_activities'),
    path('package/<int:trip_id>/', package_view, name='package_view'),
    path('package_list', package_list, name='package_list'),
    path('book/<int:trip_id>/', book_trip, name='book_trip'),
]
