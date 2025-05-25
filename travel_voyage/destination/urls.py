
from django.urls import path
from . import views

urlpatterns = [
    
    
    path('add_destination', views.add_destination, name='add_destination'),
    path('edit_destination/<int:destination_id>', views.edit_destination, name='edit_destination'),
    path('delete_destination/<int:destination_id>', views.delete_destination, name='delete_destination'),

   
]
